from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
	url(r'^signUp/', views.createUser, name='createUser'),
	url(r'^login/', views.loginUser, name='loginUser'),
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
		name='baseballRotogrindersBattersTimes'),
	url(r'^baseballRotogrindersPitchersTimes', views.baseballRotogrindersPitchersTimes,
		name='baseballRotogrindersPitchersTimes'),
	url(r'^baseballSwishAnalyticsBattersTimes', views.baseballSwishAnalyticsBattersTimes,
		name='baseballSwishAnalyticsBattersTimes'),
	url(r'^baseballSwishAnalyticsPitchersTimes', views.baseballSwishAnalyticsPitchersTimes,
		name='baseballSwishAnalyticsPitchersTimes'),
	url(r'^baseballRotogrindersRightHandedPitcherSplits', views.baseballRotogrindersRightHandedPitcherSplits,
		name='baseballRotogrindersRightHandedPitcherSplits'),
	url(r'^baseballRotogrindersLeftHandedPitcherSplits', views.baseballRotogrindersLeftHandedPitcherSplits,
		name='baseballRotogrindersLeftHandedPitcherSplits'),
	url(r'^baseballPitcherLeftHandSplitsTimes', views.baseballPitcherLeftHandSplitsTimes,
		name='baseballPitcherLeftHandSplitsTimes'),
	url(r'^baseballPitcherRightHandSplitsTimes', views.baseballPitcherRightHandSplitsTimes,
		name='baseballPitcherRightHandSplitsTimes'),
	url(r'^baseballRotogrindersLeftHandedBatterSplits', views.baseballRotogrindersLeftHandedBatterSplits,
		name='baseballRotogrindersLeftHandedBatterSplits'),
	url(r'^baseballRotogrindersRightHandedBatterSplits', views.baseballRotogrindersRightHandedBatterSplits,
		name='baseballRotogrindersRightHandedBatterSplits'),
	url(r'^baseballRotogrindersRightHandedAdvancedBatterSplits', views.baseballRotogrindersRightHandedAdvancedBatterSplits,
		name='baseballRotogrindersRightHandedAdvancedBatterSplits'),
	url(r'^baseballRotogrindersLeftHandedAdvancedBatterSplits', views.baseballRotogrindersLeftHandedAdvancedBatterSplits,
		name='baseballRotogrindersLeftHandedAdvancedBatterSplits')
]