from flask_things import dynamic_flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
#import urllib2
import scraper
from flask import jsonify
import pandas as pd
from dynamic_flask import get_avg_bikes


def station_daily(station_number):
    """Returns the average number of bikes per day for a particular bike station"""
    bikes_perday = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(len(days)):
        result = dynamic_flask.get_avg_bikes(station_number, days[i])
        bikes_perday.append(result)
    return bikes_perday

def station_hourly(station_number):
    """Returns the average number of bikes per hour for a particular station
    on a particular day"""
    bikes_perhour = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(len(days)):
        result = dynamic_flask.get_bikes_per_hour(station_number, days[i])
        bikes_perhour.append(result)
    return bikes_perhour

def get_bikes_per_hour(station_number, day):
    """Getting the hourly average bikes for a particular station on a particular day"""
    sql = "select * from availability where station_number = %s and day = %s;"
    engine = scraper.scraper.connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "/home/ubuntu/anaconda3/envs/TheForkAwakens/Assignment4-P-E-K/src/scraper/db_password.txt")
    results = engine.execute(sql, station_number, day).fetchall()
    engine.dispose()
    # Now how to sort the data by hour? 
    station_details = jsonify(stations=[dict(result) for result in results]) 
    # Every index in hours will represent it's corresponding hour - going by a 24hr clock we can have 0 up to 24 indices
    # A list of lists containing the sum of bikes so far and the counter for calculating the average? 
    hours = []
    avgs = []
    for i in range(25):
        # initialise default values
        hours[i] = [0, 0]
        
    for station in station_details:
        num_bikes = station["bikes_available"]
        last_update = station["last_updated"]
        dtime = scraper.scraper.datetime_formatter(last_update)
        hours_index = dtime[6]
        hours[hours_index][0] += num_bikes
        hours[hours_index][1] += 1 

    for hour in hours:
        avg_bikes = hour[0]/hour[1]
        avgs.append(avg_bikes)
        
    return avgs

def create_charts(station_number):
    daily_avg = station_daily(station_number)
    bikes_per_day = pd.DataFrame({'Monday': daily_avg[0], 'Tuesday': daily_avg[1], 'Wednesday': daily_avg[2], 'Thursday': daily_avg[3],
                                  'Friday': daily_avg[4], 'Saturday': daily_avg[5], 'Sunday': daily_avg[6]})
    bikes_per_day.plot(kind='bar')
        
#here avgs[0] = Avg number of bikes at 12am, avgs[1] = Avg numnber of bikes at 1am, avgs[2] = Avg number of bikes at 2am... 
# avgs[13] = Average number of bikes at 1pm, 
    
    