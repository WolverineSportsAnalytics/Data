from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import mlbOptimizer
import RotoguruScraperMLB
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
    rotowire_list = []
    our_proj = mlbOptimizer.predict()
    for lineup in our_proj:
        new_lineup = []
        for player in lineup:
            new_lineup.append(Player(player.first_name + " "+ player.last_name, player.team, "/".join(player.positions), int(player.salary)))
        rotowire_list.append(new_lineup)

    rotoguru_list = []
    our_proj = RotoguruScraperMLB.predict()
    for lineup in our_proj:
        new_lineup = []
        for player in lineup:
            new_lineup.append(Player(player.first_name + " "+ player.last_name, player.team, "/".join(player.positions), int(player.salary)))
        rotoguru_list.append(new_lineup)
    
    return render(request, 'baseball/lineups.html', context={'lineup_list':rotowire_list, 'rotoLineup': rotoguru_list} )

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
