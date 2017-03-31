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
    
        #example of writing to the db
        with connection.cursor() as cursor:
            #create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('example@email.com', 'secret-password'))
            
        #connection is not autocommit by default so you must commit to 
        #save your changes
        connection.commit()

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

    #connection to the db
    file = "db_password.txt"
    fh = open(file)
    PASSWORD = fh.readline().strip()
    connection = pymysql.connect(host = 'dublinbikeprojectdb.cun91scffwzf.eu-west-1.rds.amazonaws.com', 
                                     user = 'theForkAwakens',
                                     password = PASSWORD, 
                                     db='DublinBikeProjectDB',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            #read a single record
            sql = "SELECT * FROM bike_stations;"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    finally:    
        connection.close()
        
connect_db()
        