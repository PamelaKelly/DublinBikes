import requests
import json
from pprint import pprint

file = "c:\\Users\\pamel\\Desktop\\db-apikey.txt"
fh = open(file)
APIKEY = fh.readline().strip()

NAME = "Dublin"
URI = "https://api.jcdecaux.com/vls/v1/stations"
r = requests.get(URI, params={"apiKey": APIKEY, "contract": NAME})

pprint(json.loads(r.text))

