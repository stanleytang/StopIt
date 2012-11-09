from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import *
import json
from datetime import datetime
from django.utils.timezone import get_default_timezone
from transit.models import *
from transit.utils import get_readable_time

def index(request):
    """
    Homepage
    """
    return render(request, "index.html", locals())
    
def stop_map_search(request):
    """
    AJAX call that returns all stops in map region
    
    Request:
        -lat1
        -lon1
        -lat2
        -lon2
        
    (lat1, lon1) represents NE point of map region
    (lat2, lon2) represents SW point of map region
    
    Return (JSON object):
        -stops: [{id, name, longitude, latitude}]git 
        
    If no stops found, return empty
    """
    lat1 = Decimal(request.GET['lat1'])
    lat2 = Decimal(request.GET['lat2'])
    lon1 = Decimal(request.GET['lon1'])
    lon2 = Decimal(request.GET['lon2'])
    
    stops = Stop.objects.filter(latitude__range=(lat1, lat2),
        longitude__range=(lon1, lon2))
    output = []
    for stop in stops:
        output.append(stop.json())
    return HttpResponse(json.dumps({"stops": output}),
        mimetype='application/json')
    
def stop(request):
    """
    Stop page
    
    Request:
        -id
        
    Return (template objects):
        -stop: {name, latitude, longitude}
        -routes: [{id, name, destination, arrives_in, delay_length}]
            ---- in order of arrival_time
    """
    stop_id = request.GET.get('id', -1)
    if stop_id < 0:
        return redirect('transit.views.index')
    
    now = datetime.today()
    hour = now.hour
    minutes = now.minute
    
    # TODO - remove once we have better dummy data
    hour = 14
    minutes = 20

    stop = Stop.objects.get(id=stop_id)
    lines = Line.objects.filter(linestoplink__stop__id=stop.id)
    routes = []
    
    for line in lines:
        # need to calculate arrival_time and delay_time from buses
        links = LineStopLink.objects.filter(line=line, stop=stop).order_by('index')
        
        indices = []
        for link in list(links):
            indices.append(link.index)
        buses = Bus.objects.filter(line=line)
        soonest_arrival_in_min = 0
        soonest_found = False
        current_time_in_min = hour*60 + minutes
        delay_time = 0
        for bus in buses:
            arrival_times = json.loads(bus.arrival_times)
            for index in indices:
                arrival_time = arrival_times[index]
                bus_arrival_hour = int(arrival_time[0:2])
                bus_arrival_minutes = int(arrival_time[3:5]) + bus.delay
                bus_arrival_in_min = (bus_arrival_hour*60 + bus_arrival_minutes)
                if bus_arrival_in_min >= current_time_in_min and \
                    (bus_arrival_in_min < soonest_arrival_in_min or not \
                    soonest_found):
                
                    soonest_arrival_in_min = bus_arrival_in_min
                    delay_time = bus.delay 
                    soonest_found = True
        
        if soonest_arrival_in_min < current_time_in_min:
            continue
        
        dest = line.destination().name
        line_json = line.json()        
        line_json["arrives_in"] = soonest_arrival_in_min - current_time_in_min
        line_json["delay_length"] = delay_time
        line_json["destination"] = dest
        routes.append(line_json)
            
    routes.sort(key=lambda route: route["arrives_in"])
    # lineA = {"id": 1, "name": "Line A", "destination": "Palo Alto Train Station",
    #     "arrival_time": 5, "delay_time": 2}
    # 
    # lineB = {"id": 2, "name": "Line B", "destination": "San Antonio Shopping Center",
    #     "arrival_time": 15, "delay_time": -2}
    #     
    # lineC = {"id": 3, "name": "Line C", "destination": "SLAC",
    #     "arrival_time": 25, "delay_time": 5} 
    return render(request, "stop.html", {"stop": stop.json(), "routes": routes})
    
def route(request):
    """
    Route page
    
    Request:
        -id
        
    Return (template objects):
        -route: {id, name, destination}
        -stops: [{id, name}]
        -opposite_route: {id, name, destination}
    """
    route_id = request.GET['id']
    line = Line.objects.get(pk=route_id)
    
    links = line.linestoplink_set.order_by('index')
    
    stops = []
    for link in links:
        stop = link.stop.json()
        del stop['latitude']
        del stop['longitude']
        stops.append(stop)
    
    dest = line.destination()
    json_for_line = line.json()
    json_for_line["destination"] = dest.name
    
    opposite_route_info = {}
    if line.opposite_line:
        opposite_route_info = line.opposite_line.json()
        opposite_route_info["destination"] = \
            line.opposite_line.destination().name
        
    print opposite_route_info
    
    return render(request, "route.html", {
        "stops": stops,
        "route": json_for_line,
        "opposite_route": opposite_route_info
    })
        
def route_map(request):
    """
    Route map (with buses) page
    
    Request:
        -id
        
    Return (template objects):
        -route: {id, name}
        -start
        -destination
        -route_points: [{latitude, longitude}]
        -buses: [{id, name, latitude, longitude}]
        
    If no live buses (e.g. it is midnight) return route with empty bus_points
    """
    route_id = request.GET['id']
    line = Line.objects.get(pk=route_id)
    route = line.json()
    
    links = LineStopLink.objects.filter(line=line).order_by('index')
    
    stops = []
    for link in links:
        stop = link.stop.json()
        del stop['id']
        del stop['name']
        stops.append(stop)

    now = datetime.today()
    hour = now.hour
    minutes = now.minute
    hour = 14
    minutes = 20
    now_in_min = hour*60+minutes
    
    buses = Bus.objects.filter(line=line)
    bus_locations = []
    for bus in buses:
        last_arrival = json.loads(bus.arrival_times)[-1]
        last_arrival_in_min = int(last_arrival[0:2])*60 + int(last_arrival[3:5])
        
        if last_arrival_in_min < now_in_min:
            # if the last arrival for this bus has already passed, do not show
            continue
        
        bus_locations.append(bus.json())
        
        
        
    # TODO - we also don't show bus if first_arrival hasn't happned yet!!!!
        
    # route = {"id": 1, "name": "Line A"}
    # route_points = [
    #     {"latitude": 37.4419, "longitude": -122.1649}, # Palo Alto (start)
    #     {"latitude": 37.4290, "longitude": -122.1650}, # Galvez
    #     {"latitude": 37.4223, "longitude": -122.1629}, # Vaden
    #     {"latitude": 37.4268, "longitude": -122.1814}, # Suites
    #     {"latitude": 37.4311, "longitude": -122.1778}, # Med school
    #     {"latitude": 37.4419, "longitude": -122.1649}, # Palo Alto (destination)
    # ]
    
    return render(request, "route_map.html", {
        "route": route,
        "start": line.start().name,
        "destination": line.destination().name,
        "route_points": stops,
        "buses": bus_locations
    })
