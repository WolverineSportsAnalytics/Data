from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import sys, os
from MLB_Engine import WsaEngine
import datetime
import mysql.connector
from django.core.cache import cache

class Player:
    def __init__(self, name, team, pos, sal):
        self.name = name
        self.team = team
        self.pos = pos
        self.sal = sal 
        
# Create your views here.
def index(request):
    return render(request, 'baseball/baseball.html')

def lineups(request):


    cnx = mysql.connector.connect(user="wsa@wsabasketball",
                host="wsabasketball.mysql.database.azure.com",
                database="mlb",
                password="LeBron>MJ!")
    cursor = cnx.cursor()
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')

    gen = WsaEngine.WsaEngine()
    lineups = cache.get('MlbLineups')
    if not lineups:
        print "Query"
        lineups = gen.getAllLineups(cursor, today)
        cache.set('MlbLineups', lineups, (6*60*60))  # cache for 6 hours TODO Have WsaEngine job update Memcache when runs 

    slates = []
    op_types = []
    for line in lineups:
    	slates.append(line.slate)
    	op_types.append(line.op_type)
    	
    return render(request, 'baseball/lineups.html', context={'lineup_list':lineups, 'slates':set(slates), "op_types": set(op_types)} )

def example_lineups(request):
    example_list = [Player("Corey Kluber","CLE","P","11600"), 
                        Player("Daniel Castro", "COL", "2B", "4000"),
                        Player("Christian Villanueva", "SD", "3B", "4000"),
                        Player("Francisco Lindor", "ATL", "SS", "4300"),
                        Player("Adam Duvall", "OKC", "OF", "2800"),
                        Player("Ryan Bruan", "MIL", "OF", "3500"),
                        Player("Manuel Margot", "SD", "OF", "2800"),
                        Player("Edwin Encarnacion", "CLE", "C/1B", "3400"),
                        Player("Matt Adams", "WAS", "UTIL", "2400"),
                        ]
    return render(request, 'baseball/example.html', context={'example_list':example_list} )

@login_required
def special(request):
    return render(request, 'baseball/special.html')

if __name__ == "__main__":
    lineups([])
