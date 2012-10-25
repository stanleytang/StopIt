from django.shortcuts import render

def index(request):
    return render(request, "index.html", locals())
    
def stop(request):
    return render(request, "stop.html", locals())
    
def route(request):
    return render(request, "route.html", locals())
        
def route_map(request):
    return render(request, "route_map.html", locals())
    
# favorites