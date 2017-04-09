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


class Dynamic_Data(flask.views.MethodView):
    @app.route("/availability")

#this gives all data from most recent updated info
#delete from where to get all data
    def get_recent_dynamic_data(self):
        engine = scraper.connect_db()
        sql = "Select bikes_available from availability where (station_number,last_updated) in (SELECT station_number, max(last_updated)FROM availability group by station_number)"
        rows = engine.execute(sql).fetchall()
        print("#found {} stations", len(rows))
        x = jsonify(stations=[dict(row) for row in rows])
        return x
#below are sql queries for different requests
#I am not sure how they are used yet in flask or tied to front end
# below is the assumption that they are looking for number of bikes at station 1

sql = "Select bikes_available from availability where station_number = 1 AND (station_number,last_updated) in (SELECT station_number, max(last_updated)FROM availability group by station_number)"

#below assumption user is looking for stands available at station 1

sql = "Select stands_available from availability where station_number = 1 AND (station_number,last_updated) (SELECT station_number, max(last_updated)FROM availability group by station_number)"    
 
 
    
#         __tablename__ = 'availability'
#         station_number = db.Column('station_number', db.Integer, primary_key=True)
#         bike_stands = db.Column('bike_stands',db.Integer) 
#         bike_stands_available = db.Column('bike_stands_available', db.Integer)
#         bikes_available = db.Column('bikes_available', db.Integer)
#         last_updated = db.Column('last_updated', db.Integer, primary_key=True) 
#     day = db.Column('day',db.Unicode)
    
#Not sure how to put SQL requests in dynamic yet but below are requests

#bikes available at specific station now


if __name__=="__main__":
    app.run()

'''
Created on Apr 6, 2017

@author: Katherine
'''
