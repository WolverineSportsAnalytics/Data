from django.shortcuts import render
from django.http import HttpResponse
import constants
import mysql.connector
import datetime
import sys, os
from django.core.cache import cache
sys.path.append( os.path.dirname(os.path.realpath(__file__)) + "/WnbaEngine")
import WsaLineups, WnbaEngine

# Create your views here.
def index(request):
    return render(request, 'wnba/index.html')

def lineups(request):

    cnx = mysql.connector.connect(user="wsa@wsabasketball",
                host="wsabasketball.mysql.database.azure.com",
                database="mlb",
                password="LeBron>MJ!")
    cursor = cnx.cursor()
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')

    gen = WnbaEngine.WsaEngine()
    lineups = cache.get('WnbaLineups')
    if not lineups:
        print "Query"
        lineups = gen.getAllLineups(cursor, today)
        cache.set('WnbaLineups', lineups, (6*60*60))  # cache for 6 hours TODO Have WsaEngine job update Memcache when runs 

    slates = []
    op_types = []
    number_lineups = []
    for line in lineups:
    	slates.append(line.slate)
    	op_types.append(line.op_type)
        number_lineups.append(line.number)
    	
    return render(request, 'wnba/lineups.html', context={'lineup_list':lineups, 'slates':set(slates), "op_types": set(op_types), "num_lineups": set(number_lineups)} )

def example_lineups(request):
        class Player:
            def __init__(self, name, team, pos, sal):
                self.name = name
                self.team = team
                self.pos = pos
                self.sal = sal 

        example_list = [Player("Alex Jones","MIN","G","3100"), 
                        Player("Shekinna Stricklen", "CON", "G", "4400"),
                        Player("Brittney Sykes", "ATL", "G", "6400"),
                        Player("Sylvia Fowles", "MIN", "F", "7700"),
                        Player("Jessica Breland", "ATL", "F", "5300"),
                        Player("Crystal Langhorne", "SEA", "F", "5100"),
                        Player("Brittney Griner", "PHO", "F", "7800"),
                        ]

        return render(request, 'wnba/example.html', context={'example_list':example_list} )

