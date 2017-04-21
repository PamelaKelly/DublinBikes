 //Ideas for this code (getting the markers on the map from the json data) was adapted from code given in the lecure notes (lecutre 16-17)
// and https://gist.github.com/parth1020/4481893. Aslo from the Google map API - https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

google.charts.load("visualization", "1", {packages:["corechart"]});

// Event Listener function so that drawChart is called on click event 
$('html', 'body').click(function() {
	drawChart(data);
});

$( document ).ready(function() {
        //console.log( "document loaded" );
        getWeather();
    });
 

function getWeather(){
//call weather API from openweathermap
    var weatherdata;
    $.getJSON('http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=d3d46f56da72cd82f71b36179d95b0bd',function(data){
//    console.log("got data, ", data);
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
                //var stationNum = "{{ stations.station_number }}";
                google.maps.event.addListener(marker, 'click', (function(marker, stations) {
                    return function() {
                        if (station.banking_available == 0) {
                            station.banking_available = "No";
                        } else {
                            station.banking_available = "Yes";
                        }
						var station_number = station.station_number;
                    	var content = "Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address + "<br>" + "Banking: " + station.banking_available + "<br>";
                    	//var button = "<input type='submit' onclick='myFunction(" + station_number + ")' value='Click for more detailed information' class='submit'></input>";
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
            var content = "Station address: " + station.station_address + "<br>" + "Bikes available: " + station.bikes_available +"<br>" + "Bike stands available: " + station.bike_stands_available + "<br>";
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
		var options = {'title':'Daily Averages:', 'width': 400, 'height': 300};
		
		//instantiate and draw our chart, passing in some options
		var chart = new google.visualization.BarChart(document.getElementById('daily_div'));
		chart.draw(data_daily, options);
	}

	var jqxhr2 = $.getJSON("http://127.0.0.1:5000/charts_daily?station_number=" + station_number + "\"", null, function(data) {
		google.charts.setOnLoadCallback(drawChart(data));
	});
}	
	
	/*
	var jqxhr2 = $.getJSON("http://127.0.0.1:5000/charts?station_number=" + station_number + "\"", null, drawCharts(data)) 
	
	function drawCharts(data) {
		var data_daily = google.visualization.arrayToDataTable([
		['Day', 'Average Bikes Available', 'Average Stands Available', {role: 'style'}],
		['Monday', '{{bikes_perday[0]}}', 'green'],
		['Tuesday', '{{bikes_perday[1]}}', 'grey'],
		['Wednesday', '{{bikes_perday[2]}}', 'green'],
		['Thursday', '{{bikes_perday[3]}}', 'grey'],
		['Friday', '{{bikes_perday[4]}}', 'green'],
		['Saturday', '{{bikes_perday[5]}}', 'grey'],
		['Sunday', '{{bikes_perday[6]}}', 'green']
		]);
	
		var data_hourly = google.visualization.arrayToDataTable([
		['Hour', 'Average Bikes Available', 'Average Stands Available', {role: 'style'}],
		['12am', '{{bikes_perhour[0]}}', 'green'],
		['1am', '{{bikes_perhour[1]}}', 'grey'],
		['2am', '{{bikes_perhour[2]}}', 'green'],
		['3am', '{{bikes_perhour[3]}}', 'grey'],
		['4am', '{{bikes_perhour[4]}}', 'green'],
		['5am', '{{bikes_perhour[5]}}', 'grey'],
		['6am', '{{bikes_perhour[6]}}', 'green'],
		['7am', '{{bikes_perhour[7]}}', 'grey'],
		['8am', '{{bikes_perhour[8]}}', 'green'],
		['9am', '{{bikes_perhour[9]}}', 'grey'],
		['10am','{{bikes_perhour[10]}}', 'green'],
		['11am', '{{bikes_perhour[11]}}', 'grey'],
		['12pm', '{{bikes_perhour[12]}}', 'green'],
		['1pm', '{{bikes_perhour[13]}}', 'grey'],
		['2pm', '{{bikes_perhour[14]}}', 'green'],
		['3pm', '{{bikes_perhour[15]}}', 'grey'],
		['4pm', '{{bikes_perhour[16]}}', 'green'],
		['5pm', '{{bikes_perhour[17]}}', 'grey'],
		['6pm', '{{bikes_perhour[18]}}', 'green'],
		['7pm', '{{bikes_perhour[19]}}', 'grey'],
		['8pm', '{{bikes_perhour[20]}}', 'green'],
		['9pm', '{{bikes_perhour[21]}}', 'grey'],
		['10pm', '{{bikes_perhour[22]}}', 'green'],
		['11pm', '{{bikes_perhour[23]}}', 'grey'],
		['12pm', '{{bikes_perhour[24]}}', 'grey']
		]);
	
		var options_daily = {
			title: 'Average Daily Occupancy',
			chartArea: {width: '25%'},
			hAxis: {
				title: '',
				minValue: 0
			},
			vAxis: {
				title: ''
			}
		};
		
		var options_hourly = {
			title: 'Average Hourly Occupancy',
			chartArea: {width: '25%'},
			hAxis: {
				title: '',
				minValue: 0
			},
			vAxis: {
				title: ''
			}
		};
		
	}
		
		var chart_daily = new google.visualization.BarChart(document.getElementById("daily_div"));
		var chart_hourly = new google.visualization.BarChart(document.getElementById("hourly_div"));
		
		chart_daily.draw(data_daily, options_daily);
		chart_hourly.draw(data_hourly, options_hourly);	
	
	function loadCharts() {
			//google.load("visualization", "1", {"callback": drawCharts});
			google.load('visualization', '1', {packages: ['corechart', 'bar']});
			console.log("Callback is set");
	}
	
	setTimeout(loadCharts, 200);
}

*/

//google.load('visualization', '1', {packages: ['corechart', 'bar']});
//google.setOnLoadCallback(drawCharts);

//drawCharts()
   
//Get weather info
function displayWeather() {
 	var jqxhr = $.getJSON("http://127.0.0.1/weather", null, function(data) {
            var weather = data.weather;
            _.forEach(weather, function(weather) {
             	infowindow.setContent(weather.main);
            })
        })
}