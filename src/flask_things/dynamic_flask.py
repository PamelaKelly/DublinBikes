from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy import Table, Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://theForkAwakens:software4@DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com/db'
db = SQLAlchemy(app)


class Dynamic_Data(db.DublinBikesProjectDB):
    __tablename__ = 'availability'
    station_number = db.Column('station_number', db.Integer, primary_key=True)
    bike_stands = db.Column('bike_stands',db.Integer) 
    bike_stands_available = db.Column('bike_stands_available', db.Integer)
    bikes_available = db.Column('bikes_available', db.Integer)
    last_updated = db.Column('last_updated', db.Integer, primary_key=True) 
    day = db.Column('day',db.Unicode)

if __name__=="__main__":
    app.run()

'''
Created on Apr 6, 2017

@author: Katherine
'''
