'''
Created on 7 Apr 2017

@author: EByrn
'''
from flask import Flask
import flask, flask.views
import os
from scraper import scraper
import functools
from flask import jsonify

app = flask.Flask(__name__)

class Stations(flask.views.MethodView):
    @app.route("/stations")
    def get_stations():
        engine = scraper.connect_db()
        sql = "select * from bike_stations;"
        rows = engine.execute(sql).fetchall()
        print("#found {} stations", len(rows))
        x = jsonify(stations=[dict(row) for row in rows])
        return x
        #return flask.render_template('stations.html')



# # Getting static data
# @app.route("/stations/")
# @functools.lru_cache(maxsize=128)