from django.shortcuts import render

def index(request):
    return render(request, "maps/index.html", locals())