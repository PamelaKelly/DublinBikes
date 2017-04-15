# This will be for flask
import flask
import functools
from flask import Flask, render_template, request
from flask import jsonify
from src.scraper import scraper
from src.weather import weather_scraper
from main import Main

app = flask.Flask(__name__)

app.add_url_rule('/',
                 view_func=Main.as_view('main'),
                 methods=["GET"])
app.add_url_rule('/<page>/',
                 view_func=Main.as_view('page'),
                 methods=["GET"])

     
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404

@app.route("/stations")
def get_stations():
    engine = scraper.connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")
    sql = "select * from bike_stations;"
    rows = engine.execute(sql).fetchall()
    print("#found {} stations", len(rows))
    stations = jsonify(stations=[dict(row) for row in rows])    
    engine.dispose()
    return stations

@app.route("/weather")
def get_weather():
    engine = weather_scraper.connect_weather_db()
    sql = "select * from weather_data"
    rows = engine.execute(sql).fetchall()
    print("#found {} data points", len(rows))
    weather = jsonify(weather=[dict(row) for row in rows])
    engine.dispose()
    return weather

@app.route("/availability")
def availability():
    engine = scraper.connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")
    # change this to suit what queries we will be using
    sql = "SELECT * from availability;"
    #sql = "SELECT bike_stands_available, bikes_available FROM availability where day='Wed' and station_number='1';"
    #sql = "SELECT bike_stations.station_number, bike_stations.station_name, bike_stations.station_address, bike_stations.banking_available, availability.bike_stands, availability.bike_stands_available, availability.bikes_available FROM bike_stations INNER JOIN availability ON bike_stations.station_number=availability.station_number where availability.station_number='1';"
    rows = engine.execute(sql).fetchall()
    print("#found {} availability", len(rows))
    availability = jsonify(stations=[dict(row) for row in rows])
    engine.dispose()
    return availability

# @app.route('/result', methods = ['POST', 'GET'])
# def result():
#     if request.method == 'POST':
#         result = request.form
#         return render_template("result.html",result = result)
    
    
@app.route('/results.html', methods=['GET','POST'])
def results():
    engine = scraper.connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")
    sql = "SELECT * FROM bike_stations WHERE station_number = '{};"
    rows = engine.execute(sql).fetchall()
    posts = [dict(item=row[0], name=row[1]) for row in rows]
    engine.dispose()
    return render_template('results.html', posts=posts)


if __name__ == "__main__":
    app.run(debug=True)