from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://theForkAwakens:software4@DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com/db'
db = SQLAlchemy(app)

class Static_Data(db.DublinBikesProjectDB):
    __tablename__= 'bike_stations'
    station_number = db.Column('station_number', db.Integer, primary_key=True, db.ForeignKey('bike_stations.station_number'))
    station_name =  db.Column('station_number', db.Unicode)
    station_address = db.Column('station_address', db.Unicode)
    station_loc_lat =  db.Column('station_loc_lat', db.Float)
    station_loc_long = db.Column('station_loc_long', db.Float)
    #how to do booleans? not tinyint - smallint perhaps?
    banking_available = db.Column('banking_available',db.SmallInteger)
    bonus = db.Column('bonus', db.SmallInteger) 
    
#Check the foreign key stuff - looks pretty confusing

class Dynamic_Data(db.DublinBikesProjectDB):
    __tablename__ = 'availability'
    station_number = db.Column('station_number', db.Integer, primary_key=True, db.ForeignKey('bike_stations.station_number'))
    bike_stations = relationship("Static_Data", backref=backref("availability", uselist=False))
    bike_stands = db.Column('bike_stands',db.Integer) 
    bike_stands_available = db.Column('bike_stands_available', db.Integer)
    bikes_available = db.Column('bikes_available', db.Integer)
    last_updated = db.Column('last_updated', db.Integer, primary_key=True) 
    

@app.route("/")
def hello():
    return "hello world"

if __name__=="__main__":
    app.run()

'''
Created on Apr 6, 2017

@author: Katherine
'''
