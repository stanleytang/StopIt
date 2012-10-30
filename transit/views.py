from django.shortcuts import render

def index(request):
    """
    Homepage
    """
    return render(request, "index.html", locals())
    
def stop_map_search(request):
    """
    AJAX call that returns all stops in map region
    
    Request:
        -min_lat
        -max_lat
        -min_long
        -max_long
    
    Return (JSON):
        -stops: [stop]
    """
    return None
    
    
def stop(request):
    """
    Stop page
    
    Request:
        -id
    """
    stop_id = request.GET.get('id', 1)
    
    # if no id, should redirect to homepage
    
    # TODO (andy fang) get stop from database
    
    # temporary - using dummy data
    stop = {"name": "Stop " + str(stop_id), "latitude": 37.4419, 
        "longitude": -122.1649}
    
    lineA = {"id": 1, "name": "Line A", "destination": "Palo Alto Train Station",
        "arrival_time": 5, "delay_time": 2}
    
    lineB = {"id": 2, "name": "Line B", "destination": "San Antonio Shopping Center",
        "arrival_time": 15, "delay_time": -2}
        
    lineC = {"id": 3, "name": "Line C", "destination": "SLAC",
        "arrival_time": 25, "delay_time": 5}
    
    routes = [lineA, lineB, lineC]
    
    return render(request, "stop.html", {"stop": stop, "routes": routes})
    
def route(request):
    """
    Route page
    
    Request:
        -id
    """
    route_id = request.GET['id']
    
    # TODO (andy fang) get stop from database
    
    # temporary - using dummy data
    
    return render(request, "route.html", locals())
        
def route_map(request):
    """
    Route map (with buses) page
    
    Request:
        -id
    """
    return render(request, "route_map.html", locals())