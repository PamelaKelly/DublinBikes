# This will be for flask


from flask import Flask
from flask import jsonify
from src.scraper import scraper

app = Flask(__name__)

# app = Flask(__name__, static_url_path='/\\Users\EByrn\workspace\hellow')

# @app.route("/")
# def root():
#     return "Hello world"


@app.route("/")
def get_stations():
    engine = scraper.connect_db()
    sql = "select * from bike_stations;"
    rows = engine.execute(sql).fetchall()
    #print("#found {} stations", len(rows))
    x = jsonify(stations=[dict(rows.items()) for row in rows])
    return x
    


if __name__ == "__main__":
    app.run(debug=True)