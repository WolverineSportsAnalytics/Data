from django.contrib import admin                                                                                                                                                     
from django.conf.urls import url                                                                                                                                                     
from . import views  

app_name = 'wnba'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^lineups$', views.lineups, name='lineups'),
        url(r'^lineups/example', views.example_lineups, name='example'),
        
]
