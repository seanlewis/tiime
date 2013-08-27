#! /usr/bin/env python

"""
http://flask.pocoo.org/
Run from command line, something like:
python tiime.py
Then go to http://localhost:5000/ in your browser. Boom!
"""

from flask import Flask
from flask import render_template
import time
import requests
import urllib
import re
import json
app = Flask(__name__)

# Reads the time from the API and formats it to time-only (no dates)
utc_time_static = urllib.urlopen("http://www.timeapi.org/utc/now?\T").read()
# Reads the time from the server
# Formats server time into a nice human-readable string
server_time = time.strftime("<h1>%r - %Z<br>%A, %d %B %G</h1>")

@app.route("/<location>")
def locTime(location):
# Reads the time produced by the URL below
# Calling this here means that the time is refreshed when the page is.
	#utc_time = urllib.urlopen("http://www.timeapi.org/%s/now?\T" % (location)).read()
	# loc_data = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true" % location).read()
	loc_data = requests.get("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true" % location).text
	#need to get the coords data from json into the following variable
	#coords = json.dumps(locdata.coords)
	#pass the coords variable into the timezone URL API call

	location_data = json.loads(loc_data)
	location_coords = location_data['results'][0]['geometry']['location']
	lat = location_coords['lat']
	lng = location_coords['lng']
	
	timezone_enter = requests.get("https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=1331161200&sensor=true" % (lat, lng)).text
	
	tz_offset_raw = json.loads(timezone_enter)
	tz_offset = tz_offset_raw["rawOffset"]
	str_offset = str(tz_offset)
	return render_template("index.html", offset = str_offset, city = location.title())


@app.route("/middaytest")
def test():
# Take the two first digits of utc_time and turn them into an integer
	utc_time = urllib.urlopen("http://www.timeapi.org/utc+12/now?\T").read()
	first_digit = int(utc_time[:2])
# If the first two numbers of utc_time are above 11 it means that it's the afternoon.
	if first_digit > 11:
		return " P.M."
	else:
		return " A.M."

# App route = thing after the url
@app.route("/")
# Call this function whatever you want
def home():
	# This is what comes back when the page is requested
	return "<h1>Whats the tiime?</h1>"
	
@app.route("/servertime")
def showServerTime():
	return server_time

# dem variables.
@app.route("/say/<what>")
def say(what):
	return "<h1>%s</h1>" % (what)
	
# This is true when you run the file, not include it as a module
# If I do "import tiime" from another file, this won't be run
# But if I run this file like "python tiime.py" it will.
if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)