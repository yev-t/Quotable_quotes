from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index, name='index'), #login/registration page
	url(r'^registration$', views.registration, name='registration'), #registration process
	url(r'^login$', views.login, name='login'), #login process
	url(r'^home$', views.home, name='home'), #home page
	url(r'^logout$', views.logout, name='logout'), #logout process
	url(r'^newquote$', views.new_quote, name='new_quote'), #new quote process
	url(r'^users/(?P<user_id>\d+)$', views.user_info, name='user_info'), #user info page
	url(r'^quote/unfavorite$', views.remove_favorite, name='remove_favorite'), #un-favorite process
	url(r'^quote/favorite$', views.add_favorite, name='add_favorite'), #favorite process
]