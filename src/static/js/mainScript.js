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

                google.maps.event.addListener(marker, 'click', (function(marker, stations) {
                    return function() {
                        infoWindow.setContent("Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address);
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