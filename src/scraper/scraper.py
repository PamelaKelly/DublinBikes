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
from sqlalchemy.dialects.mysql.types import FLOAT, VARCHAR

# Need to make connection to db once and store connection in global object? - name of library? 
# Design Flaw: If I run the scraper to test it - and then run it again a few mins later - while there won't
# be duplicate entries in the database there will be duplicate files with different names because I'm 
# passing time.time() to create the filename. 

Base = declarative_base()

class Station(Base):
    __tablename__ = 'bike_stations'

    station_number = Column(Integer, primary_key=True, nullable=False)
    station_name = Column(String, nullable=False)
    station_address = Column(String, nullable=False)
    station_loc_lat = Column(FLOAT, nullable=False)
    station_loc_long = Column(FLOAT, nullable=False)
    banking_available = Column(TINYINT, nullable=False)
    bonus = Column(TINYINT, nullable=False)

    def __repr__(self):
        return """
        <Station=(station_number=%s, 
        station_name='%s',
        station_address='%s',
        station_loc_lat=%s,
        station_loc_long=%s,
        banking_available=%s,
        bonus=%s)>""" % (self.station_number, self.station_name,
                 self.station_address, self.station_loc_lat,
                 self.station_loc_long, self.banking_available,
                 self.bonus)

class Station_Dynamic(Base):
    __tablename__ = 'availability'

    station_number = Column(Integer, primary_key=True, nullable=False)
    bike_stands = Column(Integer, nullable=False)
    bike_stands_available = Column(Integer, nullable=False)
    bikes_available = Column(Integer, nullable=False)
    last_updated = Column(Integer, primary_key=True, nullable=False)
    day = Column(VARCHAR, nullable=False)


    def __repr__(self):
        return """
        <Station_Dynamic=(station_number=%s,
        bike_stands=%s, 
        bike_stands_available=%s,
        bikes_available=%s,
        last_updated=%s, 
        day = %s)>""" % (self.station_number, self.bike_stands,
                        self.bike_stands_available, self.bikes_available,
                        self.last_updated, self.day)

def datetime_formatter(info):
    """Takes the current time and returns the date, time and day of the week as a string"""
    if type(info) == float:
        dt = datetime.datetime.fromtimestamp(info).strftime('%Y-%m-%d %H-%M-%S')
        day = datetime.datetime.fromtimestamp(info).strftime('%a')
        return day, dt
    elif type(info) == str:
        return day_from_filename(info)

def day_from_filename(filename):
    word = filename.split()
    date = word[0][7:]
    new_date = ""
    if date[5:7] == '04':
        month = 'April'
    elif date[5:7] == '03':
        month = 'March'
    new_date += (month + " " + date[8:] + ", " + date[:4])
    day = datetime.datetime.strptime(new_date, '%B %d, %Y').strftime('%a')
    return day

def write_to_file(data):
    """Stores json data in a file with date and time as part of filename"""
    dt = datetime_formatter(time.time())[1]
    with open('db-data-' + dt + '.txt', 'w') as outfile:
        json.dump(data, outfile)

def connect_db(URI, PORT, DB, USER, password_file):
    #rename this function to get_engine or something
    """Connects to the database"""
    try:
        fh = open(password_file)
        PASSWORD = fh.readline().strip()
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)
        return engine
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)   

def write_to_stations(data, filename):
    #filename not used here but want to use a callback in 
    #write to file... 
    engine = connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        try:
            banking = 1 if (i['banking']) else 0
            bonus = 1 if (i['bonus']) else 0

            station = Station(station_number=i["number"],
                                    station_name=i["name"],
                                    station_address=i["address"],
                                    station_loc_lat=i["position"]["lat"],
                                    station_loc_long=i["position"]["lng"],
                                    banking_available=banking,
                                    bonus=bonus)
            
            session.add(station)
            session.commit()

        except Exception as e:
            print("Error Type: ", type(e))
            print("Error Details: ", e)
            session.rollback()
            continue
    
    session.close()
    engine.dispose()

def write_to_availability(data, day_source):
    date_time = datetime_formatter(day_source)
    day = date_time[0]
    engine = connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in data:
        try:
            station_dynamic = Station_Dynamic(station_number=int(i["number"]),
                                bike_stands=int(i["bike_stands"]),
                                bike_stands_available=int(i["available_bike_stands"]),
                                bikes_available=int(i["available_bikes"]),
                                last_updated=int(i["last_update"]),
                                day=day)

            session.add(station_dynamic)
            session.commit()
            
        except Exception as e:
            print("Error Type: ", type(e))
            print("Error details: ", e)
            session.rollback()
            continue
        
    session.close()
    engine.dispose()

def file_to_db(file, write_function):
    """ Helper function to write data from file to database
    Given the file name and the function to pass the data to"""
    try:
        with open(file, 'r') as obj:
            dataStr = json.load(obj)
            dataJson = json.loads(dataStr)
        write_function(dataJson, file)
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)
      
def multiple_files_to_db():
    try:       
        for file in os.listdir(os.getcwd()):
            if file.endswith(".txt"):
                file_to_db(file)
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)

def get_data(key_file, URI, NAME):
    """Sends the request to the Dublin bikes API and returns a json file"""
    try:
        fh = open(key_file)
        APIKEY = fh.readline().strip()
        if NAME == None:
            r = requests.get(URI, params={"apiKey": APIKEY})
        else:
            r = requests.get(URI, params={"apiKey": APIKEY, "contract": NAME})
        data = json.JSONDecoder().decode(r.text)
        return data
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)

def run_scraper():
    """Runs the overall program to scrape the data and store the data"""
    while True:
        data = get_data("db-apikey.txt", "https://api.jcdecaux.com/vls/v1/stations", "Dublin")
        write_to_file(data)
        write_to_availability(data, time.time())
        time.sleep(300)


run_scraper()

