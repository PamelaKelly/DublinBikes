# This will be for flask
from flask import Flask
from flask import jsonify
from src.scraper import scraper

app = Flask(__name__)

# Getting static data
@app.route("/")
def get_stations():
    engine = scraper.connect_db()
    sql = "select * from bike_stations;"
    rows = engine.execute(sql).fetchall()
    print("#found {} stations", len(rows))
    x = jsonify(stations=[dict(row) for row in rows])
    return x

if __name__ == "__main__":
    app.run(debug=True)