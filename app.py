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

	if request.method == "POST":
	
		# get form data - create new response
		promptID = request.form.get('id','none')
		prompt = models.Prompt.objects.get(id=promptID)
		response = models.Response()
		response.responseText = request.form.get('response','none')
		response.likes = 1

		prompt.responses.append(response)

		prompt.save()

		return redirect('/')

	else:
		# render the template
		templateData = {
			'prompts' : models.Prompt.objects.limit(1)
		}

		return render_template("main.html", **templateData)


@app.route("/prompts", methods=['GET','POST'])
def addprompt():
	
	if request.method == "POST":
		# get form data - create new idea
		prompt = models.Prompt()
		prompt.promptText = request.form.get('prompt','none')
		prompt.save()
		return redirect('/')

	else:
		templateData = {
			'prompts' : models.Prompt.objects()
		}
		return render_template("newprompt.html", **templateData)

@app.route("/thumb", methods=['POST'])
def thumb():
	if request.method == "POST":
		promptID = request.form.get('id','none')
		prompt = models.Prompt.objects.get(id=promptID)
		postResponseText = request.form.get('response','none')
		like_response = prompt.responses.objects.get(responseText=postResponseText)
		if request.form.get('do') == 'like':
			like_response.update(inc__likes=1)
		if request.form.get('do') == 'dislike':
			like_response.update(dec__likes=1)
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



	