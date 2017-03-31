import requests
import json
import time
import datetime
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import pymysql.cursors
#from IPython.display import display - not working

#Need to make connection to db once and store connection in global object? - name of library? 

#helper function to deal with datetime
def datetime_formatter(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d_%H_%M_%S')
    return dt

def write_to_file(r, dt):
    with open('db_data_' + dt + '.txt', 'w') as outfile:
        json.dump(json.JSONDecoder().decode(r.text), outfile)
    

def write_to_db():
    try:
        URI = "DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com"
        PORT = "3306"
        DB = "DublinBikeProjectDB"
        USER = "theForkAwakens"
        file = "db_password.txt"
        fh = open(file)
        PASSWORD = fh.readline().strip()
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo = True)
        sql = """INSERT INTO `bike_stations` 
        (`station_number`, `station_name`, `station_address`, 
        `station_location`, `banking_available`, `bonus`)
        VALUES (1244324234, "Trinity", "Trinity Street", 
        12321.11231, 1, 1);
        """
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)  

def run_scraper():
    file = "db-apikey.txt"
    #file = "/home/ubuntu/anaconda3/envs/TheForkAwakens/db-apikey.txt"
    fh = open(file)
    APIKEY = fh.readline().strip()
    NAME = "Dublin"
    URI = "https://api.jcdecaux.com/vls/v1/stations"
    while True:
        timestamp = time.time()
        dt = datetime_formatter(timestamp)
        r = requests.get(URI, params={"apiKey": APIKEY, "contract": NAME})
        #write_to_db(r)
        write_to_file(r, dt)
        time.sleep(300)
        
def connect_db():
    try:
        URI = "DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com"
        PORT = "3306"
        DB = "DublinBikeProjectDB"
        USER = "theForkAwakens"
        file = "db_password.txt"
        fh = open(file)
        PASSWORD = fh.readline().strip()
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo = True)
        res = engine.execute("SELECT * FROM bike_stations")
        print(res.fetchall())
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)
        
connect_db()

        