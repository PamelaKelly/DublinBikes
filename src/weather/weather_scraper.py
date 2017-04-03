import requests
import json
import time
import datetime
import os
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql.base import TINYINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql.types import FLOAT, VARCHAR, TIMESTAMP

def connect_weather_db():
    """Connects to the database"""
    try:
        URI = "weatherdb.cnmhll8wqxlt.us-west-2.rds.amazonaws.com"
        PORT = "3306"
        DB = "WeatherDB"
        USER = "Administrator"
        file = "weatherDB_password.txt"
        fh = open(file)
        PASSWORD = fh.readline().strip()
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo = True)
        return engine
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)    



def get_weather_data():
    """Sends the request to the open weather API and returns a json file"""
    file = "weather_api_key.txt"
    fh = open(file)
    APIKEY = fh.readline().strip()
    URI = "http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid="
    r = requests.get(URI, params={"apiKey": APIKEY})
    data = json.JSONDecoder().decode(r.text)
    return data


'''
Created on Apr 3, 2017

@author: Katherine
'''
