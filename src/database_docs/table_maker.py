from scraper import scraper

def make_db_tables():
    #connect to db
    engine = scraper.connect_db()
    try:
            #use database and create new record
            #create static data table
        sql = """CREATE TABLE IF NOT EXISTS bike_stations
            (station_number INT NOT NULL, 
            station_name VARCHAR(45) NOT NULL,
            station_address VARCHAR(45) NOT NULL, 
            station_location FLOAT NOT NULL, 
            banking_available TINYINT(1) NOT NULL, 
            bonus TINYINT(1), 
            PRIMARY KEY (station_number));"""
        engine.execute(sql)

        #create dynamic data table
        sql = """CREATE TABLE IF NOT EXISTS availability
            (station_number INT NOT NULL, 
            bike_stands INT NOT NULL, 
            bike_stands_available INT NOT NULL, 
            bikes_available INT NOT NULL, 
            last_updated INT(11) NOT NULL, 
            PRIMARY KEY (station_number, last_updated), 
            FOREIGN KEY (station_number) REFERENCES bike_stations(station_number));"""
        engine.execute(sql)
    except Exception as e:
        print("Error Type: ",  type(e))
        print("Error Details: ", e)

def alter_table():
    engine = scraper.connect_db()    
    try: 
        sql = "ALTER TABLE availability MODIFY COLUMN last_updated INT(11);"
        engine.execute(sql)
        sql2 = "DESCRIBE availability;"
        res = engine.execute(sql2)
        print(res.fetchall())
    except:
        print("No No No")

make_db_tables()

