# -*- coding: utf-8 -*-
from __future__ import unicode_literals	
from time import gmtime, strftime   #formating and getting timestamps
from django.shortcuts import render, redirect   #basic routing
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
	return render(request, "quotable_quotes/index.html")

def registration(request):
	registration_attempt = User.objects.registration_validation(request.POST)
	if not registration_attempt[0]:
		for key in registration_attempt[1]:
			messages.error(request, registration_attempt[1][key])
	else:
		messages.error(request, "You have succesfully registered, please log in!")
	return redirect('/')

def login(request):
	login_attempt = User.objects.login_validation(request.POST)
	if not login_attempt[0]:
		for key in login_attempt[1]:
			messages.error(request, login_attempt[1][key])
		return redirect('/')
	else:
		request.session['user_id']=login_attempt[2]['user_id']
		request.session['name']=login_attempt[2]['name']
		return redirect('/home')

def home(request):
	if not request.session['user_id']==0:
		request.session['favorites']=[]
		request.session['quotes']=[]
		faves=Quote.objects.normal_and_favorite(request.session['user_id'])
		for quote in faves[0]:
			context={
				'author':quote.author,
				'content':quote.content,
				'quote_id':quote.id,
				'poster_id':quote.user.id,
				'poster_name':quote.user.name
			}
			request.session['quotes'].append(context)
		for favorite in faves[1]:
			context2={
				'author':favorite.author,
				'content':favorite.content,
				'quote_id':favorite.id,
				'poster_id':favorite.user.id,
				'poster_name':favorite.user.name
			}
			request.session['favorites'].append(context2)
		return render(request, "quotable_quotes/home_page.html")
	else:
		messages.error(request, "Please sign in before viewing home page")
		return redirect('/')

def logout(request):
	request.session['user_id']=0
	messages.error(request, "You have been succesfully logged out")
	return redirect('/')

def new_quote(request):
	new_quote_attempt = Quote.objects.new_quote_validation(request.POST, request.session['user_id'])
	if not new_quote_attempt[0]:
		for key in new_quote_attempt[1]:
			messages.error(request, new_quote_attempt[1][key])
	else:
		messages.error(request, "New quote recorded, thanks!")
	return redirect('/home')

def user_info(request, user_id):
	info=User.objects.user_info(user_id)
	request.session["info_name"]=info[0].name
	request.session["info_review_amount"]=len(info[1])
	request.session["info_quotes"]=[]
	for quote in info[1]:
		context={
			'author':quote.author,
			'content':quote.content
		}
		request.session["info_quotes"].append(context)
	return render(request, "quotable_quotes/user_info.html")

def add_favorite(request):
	User.objects.add_favorite(request.POST)
	return redirect('/home')

def remove_favorite(request):
	User.objects.remove_favorite(request.POST)
	return redirect('/home')