from django.shortcuts import render
from django.http import HttpResponse
from decimal import *
import json
from datetime import datetime
from django.utils.timezone import get_default_timezone
from transit.models import *
import transit.constants as constants

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
        -routes: [{id, name, destination, scheduled_arrival_time,       
            actual_arrival_time, delay_length}] ---- in order of arrival_time
    """
    stop_id = request.GET.get('id', -1)
    if stop_id < 0:
        return redirect('index')
    
    now = datetime.today()
    hour = now.hour
    minutes = now.minute
    
    hour = 11
    minutes = 49

    stop = Stop.objects.get(id=stop_id)
    lines = Line.objects.filter(linestoplink__stop__id=stop.id)
    routes = []
    
    for line in lines:
        line_json = {
            "id": line.id,
            "name": line.name,
            "destination": line.destination_name
        }
        
        # need to calculate arrival_time and delay_time from buses
        index = LineStopLink.objects.get(line=line, stop=stop).index
        buses = Bus.objects.filter(line=line)
        soonest_arrival_hour = 0
        soonest_arrival_min = 0
        soonest_arrival_in_min = 0
        soonest_found = False
        current_time_in_min = hour*constants.MIN_PER_HOUR + minutes
        print 'current time = %s' % current_time_in_min
        delay_time = 0
        for bus in buses:
            arrival_times = json.loads(bus.arrival_times)
            arrival_time = arrival_times[index]
            bus_arrival_hour = int(arrival_time[0:2])
            bus_arrival_minutes = int(arrival_time[3:5]) - bus.delay
            if bus_arrival_minutes < 0:
                bus_arrival_hour = (23 if bus_arrival_hour == 0 else
                    bus_arrival_hour - 1)
                bus_arrival_minutes += constants.MIN_PER_HOUR
            
            bus_arrival_in_min = (bus_arrival_hour*constants.MIN_PER_HOUR +     
                bus_arrival_minutes)
            print 'bus arrival time = %s' %bus_arrival_in_min
            if bus_arrival_in_min >= current_time_in_min and \
                (bus_arrival_in_min < soonest_arrival_in_min or not soonest_found):
                
                soonest_arrival_in_min = bus_arrival_in_min
                soonest_arrival_hour = bus_arrival_hour
                soonest_arrival_minutes = bus_arrival_minutes
                delay_time = bus.delay
        
        if soonest_arrival_in_min < current_time_in_min:
            continue
        line_json["arrival_hour"] = soonest_arrival_hour
        line_json["arrival_minutes"] = soonest_arrival_minutes
        line_json["delay_time"] = delay_time
        routes.append(line_json)
            
    
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
    """
    route_id = request.GET['id']
    
    # TODO (andy fang) get route from database
    
    # temporary - using dummy data
    
    return render(request, "route.html", locals())
        
def route_map(request):
    """
    Route map (with buses) page
    
    Request:
        -id
        
    Return (template objects):
        -route: {id, name}
        -start
        -destination
        -stop_points: [{latitude, longitude}]
        -bus_points: [{latitude, longitude}]
        
    If no live buses (e.g. it is midnight) return route with empty bus_points
    """
    
    # dummy data
    
    # note - we can only have maximum of 10 (including start + destination) route points
    
    route = {"id": 1, "name": "Line A"}
    route_points = [
        {"latitude": 37.4419, "longitude": -122.1649}, # Palo Alto (start)
        {"latitude": 37.4290, "longitude": -122.1650}, # Galvez
        {"latitude": 37.4223, "longitude": -122.1629}, # Vaden
        {"latitude": 37.4268, "longitude": -122.1814}, # Suites
        {"latitude": 37.4311, "longitude": -122.1778}, # Med school
        {"latitude": 37.4419, "longitude": -122.1649}, # Palo Alto (destination)
    ]
    
    return render(request, "route_map.html", {"route": route, "route_points": route_points})
