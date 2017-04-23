 //Ideas for this code (getting the markers on the map from the json data) was adapted from code given in the lecure notes (lecutre 16-17)
// and https://gist.github.com/parth1020/4481893. Aslo from the Google map API - https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple
google.charts.load("visualization", "1", {packages:["corechart"]});

// Event Listener function so that drawChart is called on click event 
$('html', 'body').click(function() {
	drawChart(data);
	drawHourly(data);
});

$( document ).ready(function() {
        //console.log( "document loaded" );
        getWeather();
    });
 

function getWeather(){
//call weather API from openweathermap
    var weatherdata;
    $.getJSON('http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=d3d46f56da72cd82f71b36179d95b0bd',function(data){
    var currentWeather = data.weather[0].description;
    var current_temp=data.main.temp;
    var wind_speed=data.wind.speed;
    var icon = data.weather[0].icon;
    var iconUrl = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>");
    
    
    $("#currentWeather").html(currentWeather);
    $("#currentTemp").html(current_temp + " Degrees Centigrade");
    $("#windspeed").html(wind_speed + " m/s");
    $("#icon").html(iconUrl);
    
})
}

// Function to make the markers and display them on the map
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
				marker.metadata = {type: "point", id: station.station_number};
                google.maps.event.addListener(marker, 'click', (function(marker, stations) {
                    return function() {
                        if (station.banking_available == 0) {
                            station.banking_available = "No";
                        } else {
                            station.banking_available = "Yes";
                        }
						var station_number = station.station_number;
                    	var content = "Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address + "<br>" + "Banking: " + station.banking_available + "<br>";
                        var button = "<button onclick='showDiv(); getOccupancy(" + station_number + ")'>Click here for more detailed information!</button>";
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

//Functions to show/hide data - the occupancy info etc.
function showDiv(){
    div = document.getElementById("display");
    div.style.display = "inline-block";
}

// Gets occupancy information for a given station
function getOccupancy(station_number) {
    document.getElementById("availability").style.display = "inline-block";
    var jqxhr = $.getJSON("http://127.0.0.1:5000/station_details?station_number=" + station_number + "\"", null, function(data){
        var station_details = data.stations;
        _.forEach(station_details, function(station){
            var content = "<b><u>Station:</u></b> <br><br> Address: " + station.station_address + "<br><br>" + "<b><u>Currently there are: </u></b><br><br> Bikes available: " + station.bikes_available +"<br>" + "Bike stands available: " + station.bike_stands_available + "<br>";
            document.getElementById("availability").innerHTML = content;
        })
    });
	
	function drawChart(data) {
		//var array = JSON.parse(data_array);
		var data_array_bikes = data.daily_average_bikes;
		var data_array_stands = data.daily_average_stands;
		var data_daily = new google.visualization.DataTable(data_array_bikes);

		data_daily.addColumn('string', 'Day');
		data_daily.addColumn('number', 'Bikes');
		data_daily.addColumn('number', 'Stands');

		data_daily.addRows([
			['Monday', data_array_bikes[0], data_array_stands[0]],
			['Tuesday', data_array_bikes[1], data_array_stands[1]],
			['Wednesday', data_array_bikes[2], data_array_stands[2]],
			['Thursday', data_array_bikes[3], data_array_stands[3]],
			['Friday', data_array_bikes[4], data_array_stands[4]],
			['Saturday', data_array_bikes[5], data_array_stands[5]],
			['Sunday', data_array_bikes[6], data_array_stands[6]]
		]);
		
		//Set chart options
		var options = {'title':'Daily Averages:', 'width': 500, 'height': 400};
		
		//instantiate and draw our chart, passing in some options
		var chart = new google.visualization.BarChart(document.getElementById('daily_div'));
		chart.draw(data_daily, options);
	}

	var jqxhr2 = $.getJSON("http://127.0.0.1:5000/charts_daily?station_number=" + station_number + "\"", null, function(data) {
		google.charts.setOnLoadCallback(drawChart(data));
	});
	
	function drawHourly(data) {
		var hourly_bikes_array = data.hourly_average_bikes;
		var hourly_stands_array = data.hourly_average_stands;
		var data_hourly = new google.visualization.DataTable(hourly_bikes_array);
		
		data_hourly.addColumn('string', 'Hour');
		data_hourly.addColumn('number', 'Bikes');
		data_hourly.addColumn('number', 'Stands');
		
		var labels = ['12am-1am', '1am-2am', '2am-3am', '3am-4am', '4am-5am', '5am-6am', '6am-7am', '7am-8am', '8am-9am', '9am-10am', '10am-11am',
		'11am-12pm', '12pm-1pm', '1pm-2pm', '2pm-3pm', '3pm-4pm', '4pm-5pm', '5pm-6pm', '6pm-7pm', '7pm-8pm', '8pm-9pm', '9pm-10pm', '10pm-11pm', '11pm-12am'];
		
		var i;
		for (i = 0; i < 25; i++) {
			data_hourly.addRows([
				[labels[i], hourly_bikes_array[i], hourly_stands_array[i]]
			]);
		};	
		
		var options = {'title': 'Hourly Averages', 'width': 500, 'height': 400};
		
		var chart = new google.visualization.BarChart(document.getElementById("hourly_div"));
		chart.draw(data_hourly, options);
	}
	//var day = 'Mon';
    var day = document.getElementById('hourly_div').value;
    console.log(day);
	var jqxhr3 = $.getJSON("http://127.0.0.1:5000/charts_hourly?station_number=" + station_number + "?day=" + day + "\"", null, function(data) {
		google.charts.setOnLoadCallback(drawHourly(data));
	});
}  