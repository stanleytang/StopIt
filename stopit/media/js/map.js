function MapModule(id) {
  this.mapCanvas = document.getElementById(id);
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
  
  this.buildMap();
  this.trackUserLocation();
}

MapModule.prototype.fetchAndShowStopsInArea = function() {
  $.mobile.loading('show', {
    textVisible: true,
    text: "Searching..."
  });
  
  if (!this.alreadyDisplayed) { // temp hack - eventually, want to delete
    // all the markers and info windows and redisplay with new ones
    
    /****** TEMPORARY STOPS DUMMY DATA ********/
    
    var obj = this;
    
    window.setTimeout(function () {
      $.mobile.loading('hide');
    
      var stop1 = {
        title: "Palo Alto Station",
        latitude: 37.4419,
        longitude: -122.1649,
        id: 1,
      };
  
      var stop2 = {
        title: "The Oval",
        latitude: 37.4290,
        longitude: -122.1706,
        id: 2,
      };
  
      var stop3 = {
        title: "Vaden Health Center",
        latitude: 37.4220,
        longitude: -122.1624,
        id: 3,
      };
      
      var stop4 = {
        title: "Galvez Street",
        latitude: 37.4290,
        longitude: -122.1650,
        id: 4,
      };
  
      var stopArray = [stop1, stop2, stop3, stop4];
  
      obj.displayStopsOnMap(stopArray);
      obj.alreadyDisplayed = true;
      $("#stop_search_text").text("Redo Search In This Area");
    }, 1000);
  } else {
    window.setTimeout(function() {
      $.mobile.loading('hide');
    }, 500);
  }
}

// Set the map canvas's height/width (Google Maps needs inline height/width)
MapModule.prototype.buildMap = function() {
	// Regular web browser
	if (("standalone" in window.navigator) && !window.navigator.standalone) {
    var height = $(window).height() - $("div[data-role='header']").height() -
  	  $("div[data-role='footer']").height() + 60;
  
  // In app
  } else {
	  var height = $(window).height() - $("div[data-role='header']").height() -
  	  $("div[data-role='footer']").height();
  }	  
	  
	this.mapCanvas.style.width = '100%';
	this.mapCanvas.style.height = height + 'px';
}

MapModule.prototype.trackUserLocation = function() {
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
  		obj.map.setCenter(myLatLng);
	
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
  // Consider using 
  // http://jquery-ui-map.googlecode.com/svn/trunk/demos/jquery-google-maps-mobile.html
  
  for (index in stopsInfoArray) {
    var stop = stopsInfoArray[index];
    var stopLatLng = new google.maps.LatLng(stop.latitude, stop.longitude);
    
    // Create marker
    var stopMarker = new google.maps.Marker({
      position: stopLatLng,
      map: this.map,
      title: stop.title,
      id: stop.id
    });
    
    var busstop = stop;

    // Create popup window
    var stopInfoWindow = new google.maps.InfoWindow();
    google.maps.event.addListener(stopMarker, 'click', function() {
      var content = "<a href='/stop/?id=" + this.id + "'>" + this.title + "</a>";
      stopInfoWindow.setContent(content);
      stopInfoWindow.open(this.map, this);
    });
  }
  
  // if no results, show no results popup (TODO)
}

MapModule.prototype.clearStopsOnMap = function() {
  // https://developers.google.com/maps/documentation/javascript/overlays#RemovingOverlays
}
