from django.shortcuts import HttpResponse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
import random
import string
import Optimizer 


# Create your views here.

def index(request):
	return render(request, 'data/index.html')

def home(request):
	return render(request, 'data/home.html')

def baseball(request):
	return render(request, 'data/baseball.html')

def uploadBaseball(request):
	return render(request, 'data/baseballupload.html')

def basketball(request):
        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        lineups = Optimizer.automate()
        lineup  = []
        for line in lineups:
                lineup.append(line)
            
        players = []
        real_lineups = []
        for line in lineup:
            real_lineups.append(line)

        for line in str(real_lineups[0]).split("\n"):
            try:
                players.append(str(line).split()[1] + " " + str(line).split()[2])
            except:
                pass

        for player in players:
            print player

        return render(request, 'data/basket.html',  context={'name1':players[0], 'team1':'CHI', 'pos1':"PF",
            'name2':players[1], 'team2':'SAS', 'pos2':"PG",
            'name3':players[2], 'team3':'HOU', 'pos3':"SF",
            'name4':players[3], 'team4':'OKC', 'pos4':"PF",
            'name5':players[4], 'team5':'DET', 'pos5':"SG",
            'name6':players[5], 'team6':'GSW', 'pos6':"SF",
            'name7':players[6], 'team7':'BOS', 'pos7':"SG",
            'name8':players[7], 'team8':'LAL', 'pos8':"PG",
            'name9':players[8], 'team9':'NYK', 'pos9':"C"})


if __name__== "__main__":
            basketball()
