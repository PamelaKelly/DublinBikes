#Help for this code and explainations came from http://www.tylerlesmann.com/2009/apr/27/copying-databases-across-platforms-sqlalchemy/
import getopt
import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql
#use this when imports work
# from scraper.scraper import connect_db
# from weather.weather_scraper import connect_weather_db
def connect_make_session(URI, PORT, DB, USER, password_file):
    """Connects to the database"""
    try:
        fh = open(password_file)
        PASSWORD = fh.readline().strip()
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=False, convert_unicode=True)
        Session = sessionmaker(bind=engine)
        return Session(), engine
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)   

def pull_data(tables):
    source, sengine = connect_make_session("weatherdb.cnmhll8wqxlt.us-west-2.rds.amazonaws.com", "3306", "WeatherDB", "Administrator", "weatherDB_password.txt")
    smeta = MetaData(bind=sengine)
    destination, dengine = connect_make_session("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")

    for table_name in tables:
        print ('Processing', table_name)
        print ('Pulling schema from source server')
        table = Table(table_name, smeta, autoload=True)
        print ('Creating table on destination server')
        table.metadata.create_all(dengine)
        NewRecord = quick_mapper(table)
        columns = table.columns.keys()
        print ('Transferring records')
        for record in source.query(table).all():
            data = dict(
                [(str(column), getattr(record, column)) for column in columns]
            )
            destination.merge(NewRecord(**data))
    print ('Committing changes')
    destination.commit()

def quick_mapper(table):
    Base = declarative_base()
    class GenericMapper(Base):
        __table__ = table
    return GenericMapper

if __name__ == '__main__':
    
    pull_data('weather_data')

'''
Created on Apr 17, 2017

@author: Katherine
'''
