from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy import Table, Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
import flask, flask.views
import os
from src.scraper import scraper
import functools
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://theForkAwakens:software4@DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com/db'
db = SQLAlchemy(app)


#class Dynamic_Data(flask.views.MethodView):
    #below is wrong - the / is the page - fix later
    @app.route("/availability")

#this gives all data from most recent updated info
#delete from where to get all data
def get_recent_dynamic_data():
    engine = scraper.connect_db()
    sql = "Select bikes_available from availability where (station_number,last_updated) in (SELECT station_number, max(last_updated)FROM availability group by station_number)"
    rows = engine.execute(sql).fetchall()
    print("#found {} stations", len(rows))
    data = jsonify(stations=[dict(row) for row in rows])
    return data
#below are sql queries for different requests
#I am not sure how they are used yet in flask or tied to front end
# below is query fetching number of bikes at a station
#station now is always 1

#def get_bikes_now_available(station_number):
#    engine = scraper.connect_db()
#    sql = "Select availability.bikes_available, bike_stations.station_name from availability Inner Join bike_stations on availability.station_number = availability.station_number; Select bikes_available from availability where station_name = 'CHATHAM STREET' AND (station_number,last_updated) in (SELECT station_number, max(last_updated)FROM availability group by station_number)"
#    bikes_now = engine.execute(sql,station_number)
#    return bikes_now
    
        
#below assumption user is looking for stands available at station 1
#def get_stands_now_available(self):
#    engine = scraper.connect_db()
#    sql = "Select stands_available from availability where station_number = %s AND (station_number,last_updated) in (SELECT station_number, max(last_updated)FROM availability group by station_number)"    
#    engine.execute(sql,station_number)
    
def get_avg_bikes(station_number, day):
    """Returns the average number of bike per day"""
    engine = scraper.connect_db()
    sql = "select AVG(bikes_available) from availability where station_number = %s and day = %s;"
    avg_bikes = engine.execute(sql,station_number,day)
    engine.dispose()
    return avg_bikes

def get_avg_stands(station_number, day):
    engine = scraper.connect_db()
    sql = "select AVG(bike_stands_available) from availability where station_number = %s and day = %s;"
    avg_stands = engine.execute(sql, station_number, day)
    engine.dispose()
    return avg_stands
        
#Below returns all stations with banking  
class Static_Data(flask.views.MethodView):
#below is wrong with route
#    @app.route("/bike_stations")     
#    def where_banking(self):
#        engine = scraper.connect_db()
#        sql = "select station_number,station_address from bike_stations where banking_available > 0"
#        engine.execute(sql)
    
            
#         __tablename__ = 'availability'
#         station_number = db.Column('station_number', db.Integer, primary_key=True)
#         bike_stands = db.Column('bike_stands',db.Integer) 
#         bike_stands_available = db.Column('bike_stands_available', db.Integer)
#         bikes_available = db.Column('bikes_available', db.Integer)
#         last_updated = db.Column('last_updated', db.Integer, primary_key=True) 
#     day = db.Column('day',db.Unicode)



if __name__=="__main__":
    app.run()

'''
Created on Apr 6, 2017

@author: Katherine
'''
