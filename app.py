# -*- coding: utf-8 -*-

import os, datetime
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort

# import all of mongoengine
# from mongoengine import *
from flask.ext.mongoengine import mongoengine

# import data models
import models

app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = False

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")

# --------- Routes ----------

# this is our main page
@app.route("/", methods=['GET','POST'])
def index():

	# get Idea form from models.py
	place_form = models.PlaceForm(request.form)
	
	if request.method == "POST" and place_form.validate():
	
		# get form data - create new idea
		place = models.Place()
		place.name = request.form.get('name','none')
		place.city = request.form.get('city','none')
		place.likes = 1

		place.save()

		return redirect('/')

	else:
		# render the template
		templateData = {
			'places' : models.Place.objects.order_by('-likes').limit(5),
			'form' : place_form
		}

		return render_template("main.html", **templateData)


@app.route("/all", methods=['GET','POST'])
def index_all():

	# get Idea form from models.py
	place_form = models.PlaceForm(request.form)
	
	if request.method == "POST" and place_form.validate():
	
		# get form data - create new idea
		place = models.Place()
		place.name = request.form.get('name','none')
		place.city = request.form.get('city','none')
		place.likes = 1

		place.save()

		return redirect('/')

	else:
		# render the template
		templateData = {
			'places' : models.Place.objects.order_by('-likes'),
			'form' : place_form
		}

		return render_template("main-all.html", **templateData)

@app.route("/like", methods=['POST'])
def like():
	if request.method == "POST":
		post_name = request.form.get('name','none')
		post_city = request.form.get('city','none')
		like_place = models.Place.objects(name = post_name, city = post_city)
		like_place.update(inc__likes=1)
		return redirect('/')
		
@app.route("/dislike", methods=['POST'])
def dislike():
	if request.method == "POST":
		post_name = request.form.get('name','none')
		post_city = request.form.get('city','none')
		like_place = models.Place.objects(name = post_name, city = post_city)
		like_place.update(dec__likes=1)
		return redirect('/')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	