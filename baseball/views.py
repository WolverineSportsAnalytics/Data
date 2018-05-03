from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'baseball/baseball.html')

def lineups(request):
    context = []
    return render(request, 'baseball/lineups.html', context)

def example_lineups(request):
        class Player:
            def __init__(self, name, team, pos, sal):
                self.name = name
                self.team = team
                self.pos = pos
                self.sal = sal 
        
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


