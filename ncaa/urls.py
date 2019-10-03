from django.contrib import admin                                                                                                                                                     
from django.conf.urls import url                                                                                                                                                     
from . import views  

app_name = 'ncaa'

urlpatterns = [
        url(r'^tree$', views.tree, name='tree'),
]
