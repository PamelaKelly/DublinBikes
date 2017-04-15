
// function showStationMarkers() {
//     var map = new google.maps.Map(document.getElementById('map'), {
//         zoom: 13,
//         center: new google.maps.LatLng(53.3438, -6.2546),
//         mapTypeId: google.maps.MapTypeId.ROADMAP
//     });
//     // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple
//     var infoWindow = new google.maps.InfoWindow();
//     console.log("After map");
//     //var jqxhr = $.when($.getJSON("http://127.0.0.1:5000/stations", null), $.getJSON("http://127.0.0.1:5000/availability", null)).done(function(data, data1) {
//     var jqxhr = $.getJSON("http://127.0.0.1:5000/stations", null, function(data) {
//             var test = $.getJSON("http://127.0.0.1:5000/availability", null, function(data1) {
//             console.log("In the nest");
//             var stations = data.stations;
//             var availability = data1.availability;
//             console.log(stations);
//             console.log(data1.availability);
//             _.forEach(stations, function(station) {
//                 console.log("in the first for each loop");
//                 _.forEach(availability, function(availability) {
//                     console.log("In the second for each loop");
//                 var marker = new google.maps.Marker({
//                     position: {
//                         lat: station.station_loc_lat,
//                         lng: station.station_loc_long
//                     },
//                     map: map,
//                     title: station.station_name,
//                     station_number: station.station_number
//                 });
//                 google.maps.event.addListener(marker, 'click', (function(marker, stations, availability) {
//                     return function() {
//                         if (station.banking_available == 0) {
//                             station.banking_available = "No";
//                         } else {
//                             station.banking_available = "Yes";
//                         }
//                         var content = "Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address + "<br>" + "Banking: " + station.banking_available + "<br>";
//                         var button = "<input type='button' onclick='testBank()' value='Click for more detailed information' class='button'></input>";
//                         infoWindow.setContent(content + "<br> " + button + "<br>" + availability.bikes_available);
//                         infoWindow.open(map, marker);
//                     }
//                 })(marker, stations));
//             })
//         })
//         })
//         })
//         .fail(function() {
//             console.log("error");
//         })
// }

//showStationMarkers();

function test() {
$.when($.getJSON("http://127.0.0.1:5000/stations", null), $.getJSON("http://127.0.0.1:5000/availability", null)).done(function(data, data1) {
    console.log("test");
})
}

test();