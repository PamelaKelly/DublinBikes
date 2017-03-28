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

#helper function to deal with datetime
def datetime_formatter(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d_%H_%M_%S')
    return dt

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
        with open('db_data_' + dt + '.txt', 'w') as outfile:
            json.dump(json.JSONDecoder().decode(r.text), outfile)
        time.sleep(300)
        
def connect_db():
    try: 
        URI = "dublinbikeprojectdb.cun91scffwzf.eu-west-1.rds.amazonaws.com"
        PORT = "3306"
        DB = "dublinbikeprojectdb"
        USER = "theForkAwakens"
        file = "db_password.txt"
        fh = open(file)
        PASSWORD = fh.readline().strip()
        engine = sqla.create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo = True)
        #connection = engine.connect()
        #result = connection.execute()
        result = engine.execute("Select *")
        print(result.fetchall())
    except Exception as e:
        print("Error Type: ",  type(e))
        print("Error Details: ",  e)
        
def connect_db_2():

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
    """
        #example of writing to the db
        with connection.cursor() as cursor:
            #create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('example@email.com', 'secret-password'))
            
        #connection is not autocommit by default so you must commit to 
        #save your changes
        connection.commit()
    """
    try:
        with connection.cursor() as cursor:
            #read a single record
            sql = "SELECT *"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    finally:    
        connection.close()
        
connect_db_2()