import requests
import json
import time
import datetime

#helper function to deal with datetime
def datetime_formatter(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return dt

def run_scraper():
    file = "/home/ubuntu/anaconda3/envs/TheForkAwakens/db-apikey.txt"
    fh = open(file)
    APIKEY = fh.readline().strip()
    NAME = "Dublin"
    URI = "https://api.jcdecaux.com/vls/v1/stations"
    print(time.time())
    while True:
        timestamp = time.time()
        dt = datetime_formatter(timestamp)
        r = requests.get(URI, params={"apiKey": APIKEY, "contract": NAME})
        with open('db-data' + dt + '.txt', 'w') as outfile:
            json.dump(r.text, outfile)
        time.sleep(300)