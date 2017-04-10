# This will be for flask
import flask
import functools
from flask import Flask
from flask import jsonify
from scraper import scraper
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
    engine = scraper.connect_db()
    sql = "select * from bike_stations;"
    rows = engine.execute(sql).fetchall()
    print("#found {} stations", len(rows))
    stations = jsonify(stations=[dict(row) for row in rows])
    return stations


if __name__ == "__main__":
    app.run(debug=True)