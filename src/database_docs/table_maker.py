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
            station_loc_lat FLOAT NOT NULL,
            station_loc_long FLOAT NOT NULL, 
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
            last_updated BIGINT NOT NULL, 
            PRIMARY KEY (station_number, last_updated), 
            FOREIGN KEY (station_number) REFERENCES bike_stations(station_number));"""
        engine.execute(sql)
    except Exception as e:
        print("Error Type: ",  type(e))
        print("Error Details: ", e)

#the function to change the table / db via code and not through workbench
def alter_table():
    engine = scraper.connect_db()    
    try: 
        sql = "ALTER TABLE bike_stations CHANGE station_location station_loc_lat FLOAT NOT NULL;"
        engine.execute(sql)
        sql2 = "ALTER TABLE bike_stations ADD COLUMN station_loc_long FLOAT NOT NULL AFTER station_loc_lat;"
        engine.execute(sql2)
        sql3 = "DESCRIBE availability;"
        res = engine.execute(sql3)
        print(res.fetchall())
    except:
        print("NoooOOOooo")
        
def alter_column_datatype(table, column, data_type):
    """ Function to edit data types in database.."""
    engine = scraper.connect_db()    
    try: 
        sql = "ALTER TABLE %s MODIFY COLUMN %s %s;"
        engine.execute(sql, (table, column, data_type))
    except Exception as e:
        print("Error type: ", type(e))
        print("Error details: ", e)
        
