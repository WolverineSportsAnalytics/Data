from django.conf.urls import url

from . import views

app_name = 'data'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^baseball/$', views.baseball, name="baseball"),
	url(r'^lineups/$', views.lineups, name="lineups"),
	url(r'^lineups/example$', views.example_lineups, name="example"),
        url(r'^historicalLineups/$', views.historical, name="historical"),
	url(r'^basketball2/$', views.BasketballView.as_view(), name="basketball2"),
	url(r'^baseball/upload/$', views.uploadBaseball, name="uploadBaseball")
]
