# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import gmtime, strftime   #formating and getting timestamps
from datetime import datetime
from django.db import models
import re, bcrypt   # for hashing passwords and validations
ALIAS_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-z A-Z]+$')
# Create your models here.

class UserManager(models.Manager):
	def registration_validation(self, registration_data):
		is_valid=True
		errors={}
		if (len(registration_data['alias'])<2):
			errors['alias']="Alias needs to be atleast 2 characters long"
			is_valid=False
		elif not ALIAS_REGEX.match(registration_data['alias']):
			errors['alias']="Alias must contain only letters or numbers"
			is_valid=False
		elif (User.objects.filter(alias=registration_data['alias']).exists()):
			errors['alias']="Alias already taken, please select a different one"
			is_valid=False
		if (len(registration_data['password']))<2:
			errors['password']="Password needs to be atleast 2 characters long"
			is_valid=False
		elif registration_data['password'] != registration_data['confirm_password']:
			errors['password']="Passwords do not match"
			is_valid=False
		if (len(registration_data['name']))<2:
			errors['name']="Name needs to be atleast 2 characters long"
			is_valid=False
		elif not NAME_REGEX.match(registration_data['name']):
			errors['name']="Name must contain only letters and spaces"
			is_valid=False
		if not registration_data['date_of_birth']:
			errors['date_of_birth']="Please select a date of birth"
			is_valid=False
		if (len(registration_data['email']))<2:
			errors['email']="Please enter an e-mail"
			is_valid=False
		elif not EMAIL_REGEX.match(registration_data['email']):
			errors['email']="E-mail must be in standard format - name@host.com"
			is_valid=False
		if is_valid:
			new_registration = User.objects.create(
				alias=registration_data['alias'],
				password=bcrypt.hashpw(registration_data['password'].encode(), bcrypt.gensalt()),
				name=registration_data['name'],
				date_of_birth=registration_data['date_of_birth'],
				email=registration_data['email'],)
			new_registration.save()
		return [is_valid, errors]

	def login_validation(self, login_data):
		is_valid=True
		errors={}
		info={}
		if len(login_data['alias'])<2:
			errors['alias']="Please enter an alias that is atleast 2 characters long"
			is_valid=False
		elif len(login_data['password'])<2:
			errors['password']="Please enter a password longer than 2 characters"
			is_valid=False
		elif not User.objects.filter(alias=login_data['alias']).exists():
			errors['login_fail']="Username/password combination incorrect"
			is_valid=False
		elif not bcrypt.checkpw(login_data['password'].encode(), User.objects.get(alias=login_data['alias']).password.encode()):
			errors['login_fail']="Username/password combination incorrect"
			is_valid=False
		else:
			user=User.objects.get(alias=login_data['alias'])
			info={
				'user_id':user.id,
				'name':user.name,
			}
		return [is_valid, errors, info]

	def user_info(request, user_id):
		user=User.objects.get(id=user_id)
		quotes=Quote.objects.filter(user=user_id)
		return [user, quotes]

	def add_favorite(request, postData):
		user=User.objects.get(id=postData['user_id'])
		this_quote=Quote.objects.get(id=postData['quote_id'])
		user.favorites.add(this_quote)
		user.save()
		return True

	def remove_favorite(request, postData):
		user=User.objects.get(id=postData['user_id'])
		this_quote=Quote.objects.get(id=postData['quote_id'])
		user.favorites.remove(this_quote)
		user.save()
		return True

class QuoteManager(models.Manager):
	def new_quote_validation(self, quote_data, user_id):
		is_valid=True
		errors={}
		if len(quote_data['author'])<2:
			is_valid=False
			errors['author']="Author needs to be atleast 2 characters long"
		elif not NAME_REGEX.match(quote_data['author']):
			is_valid=False
			errors['author']="Author name can only contain letters"
		if len(quote_data['content'])<2:
			is_valid=False
			errors['content']="Quote needs to be atleast 2 characters long"
		if is_valid:
			new_quote=Quote.objects.create(
				author=quote_data['author'],
				content=quote_data['content'],
				user=User.objects.get(id=user_id))
			new_quote.save()
		return [is_valid, errors]

	def normal_and_favorite(self, user_id):
		favorites=Quote.objects.filter(favorited_by=user_id)
		quotes=Quote.objects.exclude(favorited_by=user_id)
		return [quotes, favorites]

class User(models.Model):
	alias = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	date_of_birth = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __repr__(self):
		return '<User: {}>'.format(self.alias)

class Quote(models.Model):
	author = models.CharField(max_length=255)
	content = models.TextField()
	user = models.ForeignKey(User, related_name="quotes")
	favorited_by = models.ManyToManyField(User, related_name="favorites")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = QuoteManager()
	def __repr__(self):
		return '<Quote: {}>'.format(self.author)