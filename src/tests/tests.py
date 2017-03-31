"""Scraper Tests"""
from dublin_bikes import *
import time
import unittest

def test_datetime_formatter(timestamp, correct_date):
    try:
        str_dt = scraper.datetime_formatter(timestamp)
        dt_split = str_dt.split()
        if dt_split[0] == correct_date:
            print("You have converted to the correct date")
        time = dt_split[1].split(':')
        if time[0] == correct_date[0] and time[1] == correct_date[1]:
            print("You have converted the time correctly to the nearest minute")
    except:
        print("You have an error in your datetime formatter function")
        
#sample data and test calls
#testing datetime_formatter() function
timestamp = 1490097572.2960699
test_datetime_formatter(timestamp, ['11', '59'])

    
######################################################
"""Database Tests"""

#testing entering values into the db with binding sql params
t1 = 'bike_stations'
t22 = 'availability'
values1 = (1244324244, "Trinity", "Trinity Street", 12321.11231, 1, 1)
values2 = (1244324244, 20, 15, 5, 1490996938)

######################################################
"""Flask Tests"""

######################################################
"""Do we need any front end tests here as Aonghus
did say it is harder to test and may have to be done
through inspect element tool in browswer?"""

######################################################