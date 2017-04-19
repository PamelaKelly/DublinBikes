$( document ).ready(function() {
        console.log( "document loaded" );
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