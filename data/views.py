from django.shortcuts import HttpResponse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random
import string
import Optimizer 
import datetime
import pytz
import numpy 

# Create your views here.
def index(request):
	return render(request, 'data/index.html')

def home(request):
	return render(request, 'data/home.html')

def baseball(request):
	return render(request, 'data/baseball.html')

def baskethome(request):
	return render(request, 'data/basketballhome.html')
def uploadBaseball(request):
	return render(request, 'data/baseballupload.html')


def trends(request):
	return render(request, 'data/trends.html')
def historical(request):
        return render(request, 'data/historical.html')

def example_lineups(request):
        class Player:
            def __init__(self, name, team, pos, sal):
                self.name = name
                self.team = team
                self.pos = pos
                self.sal = sal 
        
        example_list = [Player("Russell Westbrook","OKC","PG","11600"), 
                        Player("Dennis Schoder", "ATL", "PG", "6200"),
                        Player("Devin Booker", "PHO", "SG", "7200"),
                        Player("Damion Lee", "ATL", "SG", "3500"),
                        Player("Paul George", "OKC", "SF", "8200"),
                        Player("Trevor Ariza", "HOU", "SF", "5000"),
                        Player("Blake Griffen", "DET", "PF", "8600"),
                        Player("Carmelo Anthony", "OKC", "PF", "5400"),
                        Player("Alex Len", "PHO", "C", "3900"),
                        ]
        return render(request, 'data/example.html', context={'example_list':example_list} )

class LineupsView(generic.TemplateView):
    template_name = "data/basket.html"

    @method_decorator(login_required(login_url="/login/"))
    def get(self, request):

        tz = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz)

        day = now.day
        month = now.month
        year = now.year

        lineups = []
        zolineups = []
        lelineups = []
        try:
            lineups = Optimizer.automate(day, month, year,"ridge", None)
            zolineups = Optimizer.automate(day, month, year,"mlp", None)
            lelineups = Optimizer.automate(day, month, year,"le", None)
        except:
            pass
    
        return render(request, 'data/basket.html', context={'lineup_list': lineups, 'zoLineup': zolineups, 'leLineup': lelineups, 'run_dates': "Today's"})       

    def post(self, request):

        tz = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz)
        day, month, year = (0,0,0)

        if request.POST.get("day"):
            date = request.POST.get("day")
            day = int(date[8:10])
            month = int(date[5:7])
            year = int(date[0:4])
            print day, month, year

        if request.POST.get("time", None):
            day = now.day
            month = now.month
            year = now.year

        this_day = datetime.date(year=year,day=day,month=month)
        lineups = []
        zolineups = []
        lelineups = []
        try:
            lineups = Optimizer.automate(day, month, year,"simmons", None)
            zolineups = Optimizer.automate(day, month, year,"zo", None)
            lelineups = Optimizer.automate(day, month, year,"le", None)
        except:
            pass

        return render(request, 'data/basket.html', context={'lineup_list': lineups, 'zoLineup': zolineups, 'leLineup': lelineups, 'run_dates': "Today's", 'dates': this_day.strftime('%Y-%m-%d')})       


class BasketballView(generic.ListView):
    template_name = 'data/basket2.html'
    context_object_name = 'players_list'

    def get_queryset(self):

        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        tz = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz)
        day = 0
        month = 0
        year = 0

                
        print "day", type(day)
        print "Month", month
        print "Year", year
        if day == 0:

            day = now.day
            month = now.month
            year = now.year
        day = int(day)
        month = int(month)
        year = int(year)

        try:
            lineups = Optimizer.automate(day, month, year)
            lineupsle = Optimizer.automatele(day, month, year)
            lineupszo = Optimizer.automatezo(day, month, year)

            lineup  = []
            for line in lineups:
                    print "GO", line
                    lineup.append(line)
                
            players = []
            pos = []
            team = []
            real_lineups = []
            for line in lineup:
                real_lineups.append(line)

            for line in str(real_lineups[0]).split("\n"):
                try:
                    players.append(str(line).split()[1] + " " + str(line).split()[2])
                    pos.append(str(line).split()[3])
                    team.append(str(line).split()[4])

                except:
                    pass
            
            lineup  = []
            for line in lineupsle:
                    print "GO", line
                    lineup.append(line)
                
            playersLe = []
            posLe = []
            teamLe = []
            real_lineups = []
            for line in lineup:
                real_lineups.append(line)

            for line in str(real_lineups[0]).split("\n"):
                try:
                    playersLe.append(str(line).split()[1] + " " + str(line).split()[2])
                    posLe.append(str(line).split()[3])
                    teamLe.append(str(line).split()[4])

                except:
                    pass
    
            lineup  = []
            for line in lineupszo:
                    print "GO", line
                    lineup.append(line)
                
            playersZo = []
            posZo = []
            teamZo = []
            real_lineups = []
            for line in lineup:
                real_lineups.append(line)

            for line in str(real_lineups[0]).split("\n"):
                try:
                    playersZo.append(str(line).split()[1] + " " + str(line).split()[2])
                    posZo.append(str(line).split()[3])
                    teamZo.append(str(line).split()[4])

                except:
                    pass

            return players 
        
        except:
            return []
     
    

