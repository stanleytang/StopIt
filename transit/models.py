from django.db import models

# Create your models here.

# yo andy, for the route, we also need an additional array of coordinates for the path. 
# this isn't neccesarily the same as bus stops (as they need to be more specific)

# class Line:
#     name = models.CharField(max_length=100)
#     # Related-name fields
#     # bus_set - Set of buses related to this line
# 
# class Bus:
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)