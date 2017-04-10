//// comment
//console.log("gahhhh");
//var map;
//var xmlhttp = new XMLHttpRequest();
//var url = "/static/js/Dublin.json";
//xmlhttp.onreadystatechange = function() {
//    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
//        var parsedObj = JSON.parse(xmlhttp.responseText);
//        myMap(parsedObj);
//    }
//}
//xmlhttp.open("GET", url, true);
//xmlhttp.send();
//
//function myMap(obj) {
//    var map = new google.maps.Map(document.getElementById('map'), {
//        zoom: 13,
//        center: new google.maps.LatLng(53.3438, -6.2546),
//        mapTypeId: google.maps.MapTypeId.ROADMAP
//    });
//    // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple    
//    var infoWindow = new google.maps.InfoWindow();
//    var marker, i;
//    for (i = 0; i < obj.length; i++) {
//        var location = new google.maps.LatLng(obj[i].latitude, obj[i].longitude);
//        marker = new google.maps.Marker({
//            position: location,
//            map: map,
//            title: obj[i].name + " " + obj[i].number + " " + obj[i].address
//        });
//        google.maps.event.addListener(marker, 'click', (function(marker, i) {
//            return function() {
//                infoWindow.setContent("Stop name: " + obj[i].name + "<br>" + "Stop number: " + obj[i].number + "<br>" + "Address: " + obj[i].address);
//                infoWindow.open(map, marker);
//            }
//        })(marker, i));
//    }
//}

function showStationMarkers() {
var jqxhr = $.getJSON("http://127.0.0.1:5000/", function(data) {
var stations = data.stations;
console.log('stations', stations);
_.forEach(stations, function(station) {
console.log(station.name, station.number);
var marker = new google.maps.Marker({
position : {
lat : station.position_lat,
lng : station.position_lng
},
map : map,
title : station.name,
station_number : station.number
});
})
})
.fail(function() {
console.log( "error" );
})
}