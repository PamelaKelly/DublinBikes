// Ideas for this code (getting the markers on the map from the json data) was adapted from code given in the lecure notes (lecutre 16-17)
// and https://gist.github.com/parth1020/4481893. Aslo from the Google map API - https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

function showStationMarkers() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: new google.maps.LatLng(53.3438, -6.2546),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple
    var infoWindow = new google.maps.InfoWindow();
    var jqxhr = $.getJSON("http://127.0.0.1:5000/stations", null, function(data) {
            var stations = data.stations;
            _.forEach(stations, function(station) {
                var marker = new google.maps.Marker({
                    position: {
                        lat: station.station_loc_lat,
                        lng: station.station_loc_long
                    },
                    map: map,
                    title: station.station_name,
                    station_number: station.station_number
                });
                var stationNum = "{{ stations.station_number }}";
                google.maps.event.addListener(marker, 'click', (function(marker, stations) {
                    return function() {
                        if (station.banking_available == 0) {
                            station.banking_available = "No";
                        } else {
                            station.banking_available = "Yes";
                        }
                    	var content = "Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address + "<br>" + "Banking: " + station.banking_available + "<br>";
                    	var button = "<input type='button' onclick='myFunction()' value='Click for more detailed information' class='button'></input>";
                        infoWindow.setContent(content + "<br> " + button);
                        infoWindow.open(map, marker);
                    }
                })(marker, stations));
            })
        })
        .fail(function() {
            console.log("error");
        })
}

showStationMarkers();

function testBank() {
    var jqxhr = $.getJSON("http://127.0.0.1:5000/stations", null, function(data) {
        var stations = data.stations;
        _.forEach(stations, function(station){
            document.getElementById("demo").innerHTML = stations.banking_available;
        })

    })
}


function myFunction() {
    document.getElementById("demo").innerHTML = "boo";
    //"Testing testing" + "<br>" + "More info specific for that station will appear here";
    var jqxhr = $.getJSON("http://127.0.0.1:5000/availability", null, function(data){
        var availability = data.availability;
        _.forEach(availability, function(availability){
            var stationThing = "{{ availability.bike_stands_available }}";
            document.getElementById("availability").innerHTML = stationNum;

        })
    })
}

// Get weather info
function displayWeather() {
	var jqxhr = $.getJSON("http://127.0.0.1:5000/weather", null, function(data) {
            var weather = data.weather;
            _.forEach(weather, function(weather) {
            	infowindow.setContent(weather.main);
            })
        })
}

displayWeather()