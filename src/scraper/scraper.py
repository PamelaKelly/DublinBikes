import requests
import json
import time
import datetime
import sqlalchemy
from sqlalchemy import create_engine
import calendar
#from IPython.display import display - not working

#Need to make connection to db once and store connection in global object? - name of library? 

#helper function to deal with datetime
def datetime_formatter(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d_%H_%M_%S')
    return dt

def write_to_file(r, dt):
    """Writes to backup file in json format"""
    with open('db_data_' + dt + '.txt', 'w') as outfile:
        json.dump(json.JSONDecoder().decode(r.text), outfile)

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
        return engine
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)    

def write_to_db(table, values):
    """Writes rows to the database"""
    #needs to be refactored to take table name, columns and values as arguments
    try:
        #connect to db
        engine = connect_db()
        
        #write data to bike_stations table
        sql_1 = """INSERT INTO `bike_stations` 
        (`station_number`, `station_name`, `station_address`, 
        `station_location`, `banking_available`, `bonus`)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        
        #write data to availability table
        sql_2 = """INSERT INTO `availability`
        (`station_number`, `bike_stands`, `bike_stands_available`,
        `bikes_available`, `last_updated`)
        VALUES (%s, %s, %s, %s, %s);"""
        
        if table == 'bike_stations':
            sql = sql_1
        elif table == 'availability':
            sql = sql_2
        else:
            print("Error: Invalid station name given")
            return 
        
        engine.execute(sql, values)
        
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)  

def run_scraper():
    """Scrapes the dublin bikes api for json data"""
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

