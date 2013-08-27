#! /usr/bin/env python

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")
	
@app.route("/sean")
def sean():
	return "Hello"

if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)