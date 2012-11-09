from django.db import models
# yo andy, for the route, we also need an additional array of coordinates for the path. 
# this isn't neccesarily the same as bus stops (as they need to be more specific)

class Bus(models.Model):
    """
    Represents one bus that is running in a line
    """
    line = models.ForeignKey('Line')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    arrival_times = models.TextField() # stored as JSON array of military times
                                       # e.g. '["12:00", "12:59", "13:08"]'
    delay = models.IntegerField(default=0) # measured in minutes
    
    def __unicode__(self):
        return '%s (%s): %s' %(self.line.name, str(self.delay),
            self.arrival_times)
    
    def json(self):
        return {
            "id": self.id,
            "name": self.line.name,
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "delay": self.delay
        }
    
    class Meta:
        verbose_name_plural = "buses"

class Line(models.Model):
    """
    Represents a particular line (e.g. Line A for the Marguerite)
    """
    name = models.CharField(max_length=100)
    opposite_line = models.OneToOneField('Line', null=True, blank=True)
        # e.g. Counterclockwise version of a clockwise line
    # Related-name fields
    # bus_set - Set of buses related to this line
    # stops - Stops for this Line
    
    def start(self):
        """
        Return the first Stop for the line
        """
        return list(self.linestoplink_set.order_by('index'))[0].stop
    
    def destination(self):
        """
        Return the last Stop for the line
        """
        return list(self.linestoplink_set.order_by('index'))[-1].stop
    
    def __unicode__(self):
        return self.name
    
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class LineStopLink(models.Model):
    """
    Object representing underlying join table for Line and Stop
    """
    line = models.ForeignKey(Line)
    stop = models.ForeignKey('Stop')
    index = models.IntegerField()
    
    def __unicode__(self):
        return '%s <--> (%s) %s' %(self.line.name, str(self.index), self.stop.name)


class Stop(models.Model):
    """
    Represents a location where a bus will stop to pick up people
    A stop can be part of multiple lines
    """
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    lines = models.ManyToManyField(Line, through=LineStopLink,
        related_name='stops')
    
    def __unicode__(self):
        return self.name
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'longitude': str(self.longitude),
            'latitude': str(self.latitude)
        }