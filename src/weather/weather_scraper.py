import time
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql.base import TINYINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql.types import FLOAT, VARCHAR
import scraper.scraper

Base = declarative_base()

class weather(Base):
    __tablename__ = 'weather_data'
    
    date_time = Column(FLOAT, primary_key=True, nullable=False)
    temp = Column(FLOAT, nullable=False)
    temp_max = Column(FLOAT, nullable=False)
    temp_min = Column(FLOAT, nullable=False)
    humidity = Column(Integer, nullable=False)
    main = Column(VARCHAR(45), nullable=False)
    weather_description = Column(VARCHAR(45), nullable=False)
    wind_speed = Column(Integer, nullable=False)
    
    def __repr__(self):
        return """
        <Weather=(
        date_time=%d,
        temp=%d,
        temp_max=%d,
        temp_min=%d,
        humidity=%d,
        main=%d,
        weather_description='%s',
        wind_speed=%d)>""" % (self.date_time, self.temp,
                         self.temp_max, self.temp_min,
                         self.humidity, self.main,
                         self.weather_description, self.wind_speed)
    
def connect_weather_db():
    """Connects to the database"""
    try:
        engine = scraper.scraper.connect_db("weatherdb.cnmhll8wqxlt.us-west-2.rds.amazonaws.com", "3306", "WeatherDB", "Administrator", "/home/ubuntu/anaconda3/envs/TheForkAwakens/Assignment4-P-E-K/src/weather/weatherDB_password.txt")
        return engine
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)    

def write_to_weather_db(data):
    """Creates SQLAlchemy objects from json data and pushes these objects to the db as rows"""

    engine = connect_weather_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        weather_instance = weather(date_time=data["dt"],
			temp=data["main"]["temp"],
			temp_max=data["main"]["temp_max"],
			temp_min=data["main"]["temp_min"],
			humidity=data["main"]["humidity"],
			main=data["weather"][0]["main"],
			weather_description=data["weather"][0]["description"],
			wind_speed=data["wind"]["speed"])  

        session.add(weather_instance)
        session.commit()
        session.close()
        engine.dispose()   

    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)
        session.close()
        engine.dispose()  

def get_weather_data():
    """Sends the request to the open weather API and returns a json file"""
    try:
        data = scraper.scraper.get_data("/home/ubuntu/anaconda3/envs/TheForkAwakens/Assignment4-P-E-K/src/weather/weather_api_key.txt", "http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=", NAME=None)
        return data
    except Exception as e:
        print("Error type: ", type(e))
        print("Error Details: ", e)

def run_weather_scraper():
    while True:
        data = get_weather_data()
        write_to_weather_db(data)
        scraper.scraper.write_to_file(data)
        time.sleep(1800)

#run_weather_scraper() # finished collecting data