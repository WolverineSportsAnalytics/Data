from django.contrib import admin                                                                                                                                                     
from django.conf.urls import url                                                                                                                                                     
from . import views  

app_name = 'baseball'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^lineups$', views.lineups, name='lineups'),
        
]
