from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
	url(r'^login/', views.login, name='login'),
	url(r'^baseballRotowireData/', views.baseballRotowireData, name='baseballRotowireData'),
	url(r'^baseballRotogrindersBatterData/', views.baseballRotogrindersBatterData,
		name='baseballRotogrindersBatterData'),
	url(r'^baseballRotogrindersPitcherData/', views.baseballRotogrindersPitcherData,
		name='baseballRotogrindersPitcherData'),
	url(r'^baseballSwishAnalyticsBatterData', views.baseballSwishAnalyticsBatterData,
		name='baseballSwishAnalyticsBatterData'),
	url(r'^baseballSwishAnalyticsPitcherData', views.baseballSwishAnalyticsPitcherData,
		name='baseballSwishAnalyticsPitcherData'),
	url(r'^baseballRotowireTimes', views.baseballRotowireTimes, name='baseballRotowireTimes'),
	url(r'^baseballRotogrindersBattersTimes', views.baseballRotogrindersBattersTimes,
		name='baseballRotogrindersBattersTimes')
]