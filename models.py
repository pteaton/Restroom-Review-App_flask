from peewee import *
import datetime

DATABASE = SqliteDatabase('reviews.sqlite')

class User(Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField(unique=True)


class Review(Model):
	title = CharField()
	date_posted = datetime()
	review = CharField()
	posted_by = ForeignKeyField(User, backref='reviews')
	location = CharField()

class Meta:
	database = DATABASE

def initialize():
	DATABASE.connect()

DATABASE.create_tables([User, Review], safe=True)
print("DB connected and created tables")

DATABASE.close()