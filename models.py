# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

class Place(Document):

	name = StringField(max_length=120, required=True, verbose_name="Pizza Place:", help_text="Please enter the name:")
	city = StringField(max_length=120, required=True, verbose_name="City:", help_text="Please enter the city name:")
	
PlaceForm = model_form(Place)

	

