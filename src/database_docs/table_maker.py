import pymysql 

def make_db_tables():
    #connect to db
    file = "dbPassword.txt"
    fh = open(file)
    PASSWORD = fh.readline().strip()
    conn=pymysql.connect(host="dublinbikeprojectdb.cun91scffwzf.eu-west-1.rds.amazonaws.com",
                             user="theForkAwakens",password= PASSWORD, db= 'DublinBikeProjectDB',
                             port = 3306, charset= "utf8mb4", 
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
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
            cursor.execute(sql)
    
        #must commit to save changes
        conn.commit()

        #create dynamic data table
        with conn.cursor() as cursor:
            sql = """CREATE TABLE IF NOT EXISTS availability
            (station_number INT NOT NULL, 
            bike_stands INT NOT NULL, 
            bike_stands_available INT NOT NULL, 
            bikes_available INT NOT NULL, 
            last_updated TIMESTAMP NOT NULL, 
            PRIMARY KEY (station_number, last_updated), 
            FOREIGN KEY (station_number) REFERENCES bike_stations(station_number));"""
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
        
#make_db_tables()
