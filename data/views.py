import matplotlib.pyplot as plt
from django.shortcuts import HttpResponse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import random
import string
import Optimizer 
import datetime
import pytz
import matplotlib 
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

@csrf_exempt

def trends(request):

	t = numpy.arange(0.0, 2.0, 0.01)
	s = 1 + numpy.sin(2*numpy.pi*t)
	plt.plot(t, s)
	
	plt.xlabel('Time (Days)')
	plt.ylabel('Winnings ($)')
	plt.title('Going to get our Bands Up')
	plt.grid(True)
	plt.savefig("WSADataPortal/static/test.png")
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

def lineups(request):

        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        tz = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz)
        day = 0
        month = 0
        year = 0
        if request.method == "POST":
                print request.POST.get("time", None)
                

                
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
        except:
            return render(request, 'data/basket.html', context={})       



        return render(request, 'data/basket.html',  context={'name1_1':players[0], 'team1_1':team[0], 'pos1_1':pos[0],
            'name2_1':players[1], 'team2_1':team[1],'pos2_1':pos[1],
            'name3_1':players[2], 'team3_1':team[2], 'pos3_1':pos[2],
            'name4_1':players[3], 'team4_1':team[3], 'pos4_1':pos[3],
            'name5_1':players[4], 'team5_1':team[4], 'pos5_1':pos[4],
            'name6_1':players[5], 'team6_1':team[5], 'pos6_1':pos[5],
            'name7_1':players[6], 'team7_1':team[6], 'pos7_1':pos[6],
            'name8_1':players[7], 'team8_1':team[7], 'pos8_1':pos[7],
            'name9_1':players[8], 'team9_1':team[8], 'pos9_1':pos[8],
            'name1_2':playersLe[0], 'team1_2':teamLe[0], 'pos1_2':posLe[0],
            'name2_2':playersLe[1], 'team2_2':teamLe[1], 'pos2_2':posLe[1],
            'name3_2':playersLe[2], 'team3_2':teamLe[2], 'pos3_2':posLe[2],
            'name4_2':playersLe[3], 'team4_2':teamLe[3], 'pos4_2':posLe[3],
            'name5_2':playersLe[4], 'team5_2':teamLe[4], 'pos5_2':posLe[4],
            'name6_2':playersLe[5], 'team6_2':teamLe[5], 'pos6_2':posLe[5],
            'name7_2':playersLe[6], 'team7_2':teamLe[6], 'pos7_2':posLe[6],
            'name8_2':playersLe[7], 'team8_2':teamLe[7], 'pos8_2':posLe[7],
            'name9_2':playersLe[8], 'team9_2':teamLe[8], 'pos9_2':posLe[8],
            'name1_3':playersZo[0], 'team1_3':teamZo[0], 'pos1_3':posZo[0],
            'name2_3':playersZo[1], 'team2_3':teamZo[1], 'pos2_3':posZo[1],
            'name3_3':playersZo[2], 'team3_3':teamZo[2], 'pos3_3':posZo[2],
            'name4_3':playersZo[3], 'team4_3':teamZo[3], 'pos4_3':posZo[3],
            'name5_3':playersZo[4], 'team5_3':teamZo[4], 'pos5_3':posZo[4],
            'name6_3':playersZo[5], 'team6_3':teamZo[5], 'pos6_3':posZo[5],
            'name7_3':playersZo[6], 'team7_3':teamZo[6], 'pos7_3':posZo[6],
            'name8_3':playersZo[7], 'team8_3':teamZo[7], 'pos8_3':posZo[7],
            'name9_3':playersZo[8], 'team9_3':teamZo[8], 'pos9_3':posZo[8]})
           

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
     
    

