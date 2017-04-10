// //// comment
// //console.log("gahhhh");
// var map;
// var xmlhttp = new XMLHttpRequest();
// var url = $.getJSON("http://127.0.0.1:5000/stations");
// //var url = "/static/js/Dublin.json";
// xmlhttp.onreadystatechange = function() {
//    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
//        var parsedObj = JSON.parse(xmlhttp.responseText);
//        myMap(parsedObj);
//    }
// }
// // xmlhttp.open("GET", url, true);
// // xmlhttp.send();

// console.log("test");
// function myMap(obj) {
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
// }


function showStationMarkers() {
	var map = new google.maps.Map(document.getElementById('map'), {
       zoom: 13,
       center: new google.maps.LatLng(53.3438, -6.2546),
       mapTypeId: google.maps.MapTypeId.ROADMAP
   });
var jqxhr = $.getJSON("http://127.0.0.1:5000/stations", null, function(data) {
var stations = data.stations;
_.forEach(stations, function(station) {
console.log(station.station_name);
var marker = new google.maps.Marker({
position : {
lat : station.station_loc_lat,
lng : station.station_loc_long
},
map : map,
title : station.station_name,
station_number : station.station_number
});
})
})
.fail(function() {
console.log( "error" );
})
}

showStationMarkers();



// marker.addListener("click", function(){
// infoWindow.setContent("Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_addres);
//                infoWindow.open(map, marker);
//            });



// function showStationMarkers() {
// 	var map = new google.maps.Map(document.getElementById('map'), {
//        zoom: 13,
//        center: new google.maps.LatLng(53.3438, -6.2546),
//        mapTypeId: google.maps.MapTypeId.ROADMAP
//    });
// $.getJSON("http://127.0.0.1:5000/stations", null, function(data) {
// if ('stations' in data) {
// var stations = data.stations;
// console.log('stations', stations);
// _.forEach(stations, function(station) {
// console.log(station.name, station.number);
// var marker = new google.maps.Marker({
// position : {
// lat : station.position_lat,
// lng : station.position_lng
// },
// map : map,
// title : station.name,
// station_number : station.number
// });
// google.maps.event.addListener(marker, 'click', (function(marker, i) {
//            return function() {
//                infoWindow.setContent("Stop name: " + obj[i].name + "<br>" + "Stop number: " + obj[i].number + "<br>" + "Address: " + obj[i].address);
//                infoWindow.open(map, marker);
//            }
//        })(marker, i));
// });
// }
// });
// }

// showStationMarkers();