from flask import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

if __name__=="__main__":
    app.run()

'''
Created on Apr 6, 2017

@author: Katherine
'''
