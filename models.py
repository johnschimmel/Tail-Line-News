# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

class Response(EmbeddedDocument):
	responseText = StringField(max_length=120, required=True, verbose_name="Response:", help_text="Please enter a response.")
	likes = IntField()

class Comment(EmbeddedDocument):
	commentText = StringField(max_length=120, required=True, verbose_name="Comment:", help_text="Please enter a Comment.")
	likes = IntField()
	
class Prompt(Document):
	promptText = StringField(max_length=150, required=True, verbose_name="Prompt:", help_text="Please enter a prompt.")
	responses = ListField( EmbeddedDocumentField(Response) )
	comments = ListField( EmbeddedDocumentField(Comment) )