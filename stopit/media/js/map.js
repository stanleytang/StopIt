function MapModule(id, noFooter) {
  this.markersArray = [];
  
  this.mapCanvas = document.getElementById(id);
  if (!this.mapCanvas) return;
  this.map = new google.maps.Map(
    this.mapCanvas,
    {
      zoom: 14,
      // initially center on Stanford
      center: new google.maps.LatLng(37.4225, -122.1653),
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      zoomControl: true,
      zoomControlOptions: {
         style: google.maps.ZoomControlStyle.LARGE
      }
    }
  );
  
  this.infoWindow = new google.maps.InfoWindow();
  
  this.buildMap(noFooter);
  this.trackUserLocation(noFooter);
}

MapModule.prototype.fetchAndShowStopsInArea = function() {
  $.mobile.loading('show', {
    textVisible: true,
    textonly: false,
    text: "Searching..."
  });
  
  if (this.alreadyDisplayed) { 
    this.clearStopsOnMap();
  } else {
    this.alreadyDisplayed = true;
    $("#stop_search_text").text("Redo Search In This Area");
  }
  
  debugger;
  
  var bounds = this.map.getBounds();
  var swBounds = bounds.getSouthWest();
  var neBounds = bounds.getNorthEast();
  
  var lat1 = swBounds.lat();
  var lon1 = swBounds.lng();
  
  var lat2 = neBounds.lat();
  var lon2 = neBounds.lng();

  var request = $.ajax({
    url: "/stop_map_search/?lat1=" + lat1 +"&lon1=" + lon1 + "&lat2=" + lat2 +
      "&lon2=" + lon2
  });
  
  var obj = this;

  request.done(function(msg) {
    $.mobile.loading('hide');
     
    var json = msg;
    
    // If empty, show no results found message
    if (!json || !json["stops"].length) {
      $.mobile.loading('show', {
        textonly: true,
        textVisible: true,
        text: "No stops found in this area"
      });
       
      window.setTimeout(function() {
        $.mobile.loading('hide');
      }, 3000);
    } else {
      obj.displayStopsOnMap(json["stops"]);
    }
  });
  
  request.fail(function(jqXHR, textStatus) {    
    $.mobile.loading('show', {
      textonly: true,
      textVisible: true,
      text: "Error fetching stops. Please try again"
    });
     
    window.setTimeout(function() {
      $.mobile.loading('hide');
    }, 3000);
  });
}

// Set the map canvas's height/width (Google Maps needs inline height/width)
MapModule.prototype.buildMap = function(noFooter) {
	// Regular web browser
	if (("standalone" in window.navigator) && !window.navigator.standalone) {
    var height = $(window).height() - 44 - 47 + 60; 
      // 44 is header, 47 is footer, 60 is web browser header
  
  // In app
  } else {
	  var height = $(window).height() - 44 - 47;
  }	  
  
  if (noFooter) height += 47;
	  
	this.mapCanvas.style.width = '100%';
	this.mapCanvas.style.height = height + 'px';
}

MapModule.prototype.trackUserLocation = function(noFooter) {
  var useragent = navigator.userAgent;
  var obj = this;
	
	var displayUserLocationOnMap = function(position) {
    // Create a new LatLng object for every position update
	  var myLatLng = new google.maps.LatLng(
  	  position.coords.latitude, 
  	  position.coords.longitude
  	);

  	// Build entire marker if first time 
  	if (!obj.locationMarker) {
  		// Define our custom marker image
  		var image = new google.maps.MarkerImage(
  			'/media/images/bluedot.png',
  			null, // size
  			null, // origin
  			new google.maps.Point( 8, 8 ), // anchor (move to center of marker)
  			new google.maps.Size( 17, 17 ) // scaled size (for Retina display icon)
  		);

  		// Then create the new marker
  		obj.locationMarker = new google.maps.Marker({
  			flat: true,
  			icon: image,
  			map: obj.map,
  			optimized: false,
  			position: myLatLng,
  			title: 'My location',
  			visible: true
  		});
		
  		// Center map view
  		if (!noFooter) {
  		  obj.map.setCenter(myLatLng);
		  }
	
  	// Just change marker position on subsequent passes
  	} else {
  		obj.locationMarker.setPosition(myLatLng);
  	}
  }
  
  var handleLocationError = function(error) {
    var errorMessage = [ 
  		'We are not quite sure what happened.',
  		'Sorry. Permission to find your location has been denied.',
  		'Sorry. Your position could not be determined.',
  		'Sorry. Timed out.'
  	];
  	alert(errorMessage[error.code]);
  }
  
  // Allow iPhone or Android to track movement
	if (useragent.indexOf('iPhone') !== -1 || 
	    useragent.indexOf('Android') !== -1 ) {
		navigator.geolocation.watchPosition( 
		  displayUserLocationOnMap, 
			handleLocationError, 
			{ 
				enableHighAccuracy: true, 
				maximumAge: 30000, 
				timeout: 27000 
			}
		);			

	// Or let other geolocation capable browsers to get their static position
	} else if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
		  displayUserLocationOnMap, 
		  handleLocationError
		);
	}
}

MapModule.prototype.displayStopsOnMap = function(stopsInfoArray) {  
  for (index in stopsInfoArray) {
    var stop = stopsInfoArray[index];
    var stopLatLng = new google.maps.LatLng(stop.latitude, stop.longitude);

    // Create marker
    var stopMarker = new google.maps.Marker({
      position: stopLatLng,
      map: this.map,
      title: stop.name,
      id: stop.id
    });

    this.markersArray.push(stopMarker);
    
    var obj = this;
    
    // Create popup window
    google.maps.event.addListener(stopMarker, 'click', function() {
      var content = "<a href='/stop/?id=" + this.id + "'>" + this.title + "</a>";
      obj.infoWindow.setContent(content);
      obj.infoWindow.open(this.map, this);
    });
  }
}

MapModule.prototype.clearStopsOnMap = function() {
  if (this.markersArray) {
    for (i in this.markersArray) {
      this.markersArray[i].setMap(null);
    }
    this.markersArray.length = 0;
  }
}

MapModule.prototype.displayRealTimeRouteData = function(waypoints, 
                                                        buses,
                                                        startName,
                                                        destinationName) {
  this.displayRouteOnMap(waypoints, startName, destinationName);
  this.displayBusesOnMap(buses);
}

MapModule.prototype.displayRouteOnMap = function(waypoints, startName, destinationName) {
  var directionsDisplay = new google.maps.DirectionsRenderer({
    suppressMarkers: true,
  });
  var directionsService = new google.maps.DirectionsService();
  
  directionsDisplay.setMap(this.map);
  
  var origin = waypoints[0].location;
  var destination = waypoints[waypoints.length - 1].location;
  var editedWaypoints = waypoints.slice(1, waypoints.length - 1);

  var request = {
    origin: origin,
    destination: destination,
    waypoints: editedWaypoints,
    optimizeWaypoints: false,
    travelMode: google.maps.DirectionsTravelMode.DRIVING
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    }
  });
  
  var obj = this;
  
  // Add start marker
  var startMarker = new google.maps.Marker({
    position: origin,
    map: this.map,
    title: startName
  });
  
  google.maps.event.addListener(startMarker, 'click', function() {
    if (startName == destinationName) {
      var content = "<b>Start/Destination:</b> " + startName;
    } else {
      var content = "<b>Start:</b> " + startName;
    }
    obj.infoWindow.setContent(content);
    obj.infoWindow.open(this.map, this);
  });
  
  if (startName === destinationName) return;
  
  // Add destination marker
  var destinationMarker = new google.maps.Marker({
    position: destination,
    map: this.map,
    title: destinationName
  });
    
  google.maps.event.addListener(destinationMarker, 'click', function() {
    var content = "<b>Destination:</b> " + destinationName;
    obj.infoWindow.setContent(content);
    obj.infoWindow.open(this.map, this);  
  });
}

MapModule.prototype.displayBusesOnMap = function(buses) {
	var image = new google.maps.MarkerImage(
		'/media/images/busIcon.png',
		null, // size
		null, // origin
		new google.maps.Point( 9, 9 ), // anchor (move to center of marker)
		new google.maps.Size( 19, 19 ) // scaled size (for Retina display icon)
	);
    
  for (var i = 0; i < buses.length; i++) {
    var location = buses[i].location;
    
    var delay = buses[i].delay;
    if (delay > 0) {
      var delayText = 
        "<span style='color:red'>" + delay + " mins late</span>";
    } else if (delay < 0) {
      var delayText =  "<span style='color:blue'>" + Math.abs(delay) + 
        " mins early</span>";
    } else {
      var delayText = "On time";
    }
    
    // Create marker
    var busMarker = new google.maps.Marker({
      position: location,
      map: this.map,
      icon: image,
      flat: true,
      busName: buses[i].name,
      delayText: delayText
    });
    
    var obj = this;
    
    // Create popup window
    google.maps.event.addListener(busMarker, 'click', function() {
      var content = "<b>" + this.busName + "</b><br />" + this.delayText;
      obj.infoWindow.setContent(content);
      obj.infoWindow.open(this.map, this);
    });   
  }
}



