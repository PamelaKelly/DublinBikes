from src.weather import weather_scraper
def make_weatherdb_tables():
    #connect to db
    engine = weather_scraper.connect_weather_db()
    try:
            #use database and create new record
        sql = """CREATE TABLE IF NOT EXISTS weather_data
            (date_time FLOAT NOT NULL,
            temp FLOAT NOT NULL,
            temp_max FLOAT NOT NULL,
            temp_min FLOAT NOT NULL,
            humidity INT NOT NULL,
            main VARCHAR(45) NOT NULL,
            weather_description VARCHAR(45) NOT NULL,
            wind_speed INT NOT NULL,
            PRIMARY KEY (date_time));"""
        engine.execute(sql)
        
    except Exception as e:
        print("Error Type: ",  type(e))
        print("Error Details: ", e)
        
make_weatherdb_tables()