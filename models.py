import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
	DATABASE = SqliteDatabase('reviews.sqlite')


class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField()

	class Meta:
		database = DATABASE


class Review(Model):
	title = CharField()
	date_posted = DateTimeField(default=datetime.datetime.now)
	review = TextField()
	posted_by = ForeignKeyField(User, backref='reviews')
	location = CharField()

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Review], safe=True)
	print("DB connected and created tables")
	DATABASE.close()