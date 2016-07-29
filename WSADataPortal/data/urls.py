from django.conf.urls import url

from . import views

app_name = 'data'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^baseball/$', views.baseball, name="baseball"),
	url(r'^baseball/upload/$', views.uploadBaseball, name="uploadBaseball")
]