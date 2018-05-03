from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'wnba/index.html')

def lineups(request):
    context = []
    return render(request, 'wnba/lineups.html', context)

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


