import requests
import json
from pprint import pprint
import time
import datetime

#helper function to deal with datetime
def datetime_formatter(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return dt

file = "c:\\Users\\pamel\\Desktop\\db-apikey.txt"
fh = open(file)
APIKEY = fh.readline().strip()
NAME = "Dublin"
URI = "https://api.jcdecaux.com/vls/v1/stations"
i = 0
print(time.time())
while True:
    r = requests.get(URI, params={"apiKey": APIKEY, "contract": NAME})
    pprint(json.loads(r.text))
    with open('db-data' + str(i) + '.txt', 'w') as outfile:
        json.dump(r.text, outfile)
    i += 1
    time.sleep(300)

pprint(json.loads(r.text))