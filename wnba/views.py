from django.shortcuts import render
from django.http import HttpResponse
import Optimizer
import constants
import mysql.connector
import datetime
 

# Create your views here.
def index(request):
    return render(request, 'wnba/index.html')

def lineups(request):
        class Player:
            def __init__(self, name, team, pos, sal):
                self.name = name
                self.team = team
                self.pos = pos
                self.sal = sal 

    	cnx = mysql.connector.connect(user=constants.testUser,
                                  host=constants.testHost,
                                  database=constants.testName,
                                  password=constants.testPassword)
    	cursor = cnx.cursor()
        
        now = datetime.datetime.now()

        print ("_______________________________________________________________________")
        try:
	    our_proj = Optimizer.optimize(now.day, now.month, now.year, cursor, "simmonsProj")
        except:
            print "Not up"

        example_list = []
        for lineup in our_proj:
            new_lineup = []
            print ("__________")
            for player in lineup:
                print player.first_name
                new_lineup.append(Player(player.first_name + player.last_name, player.team, player.positions[0], player.salary))
            example_list.append(new_lineup)

	our_proj = Optimizer.optimize(now.day, now.month, now.year, cursor, "rotowireProj")
        rotowire_list = []
        for lineup in our_proj:
            new_lineup = []
            for player in lineup:
                new_lineup.append(Player(player.first_name + player.last_name, player.team, player.positions[0], player.salary))
            rotowire_list.append(new_lineup)
        
        return render(request, 'wnba/lineups.html', context={'lineup_list':example_list, 'rotoLineup': rotowire_list} )

def example_lineups(request):
        class Player:
            def __init__(self, name, team, pos, sal):
                self.name = name
                self.team = team
                self.pos = pos
                self.sal = sal 

        Optimizer.optimize(cusror, cnx, "simmonsProj")
        
        example_list = [Player("Alex Jones","MIN","G","3100"), 
                        Player("Shekinna Stricklen", "CON", "G", "4400"),
                        Player("Brittney Sykes", "ATL", "G", "6400"),
                        Player("Sylvia Fowles", "MIN", "F", "7700"),
                        Player("Jessica Breland", "ATL", "F", "5300"),
                        Player("Crystal Langhorne", "SEA", "F", "5100"),
                        Player("Brittney Griner", "PHO", "F", "7800"),
                        ]

        return render(request, 'wnba/example.html', context={'example_list':example_list} )

