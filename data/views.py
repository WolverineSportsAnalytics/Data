from django.shortcuts import HttpResponse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
import random
import string
import Optimizer 
import datetime
import pytz


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
        tz = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz)
        lineups = Optimizer.automate(now.day, now.month, now.year)
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

        return render(request, 'data/basket.html',  context={'name1':players[0], 'team1':team[0], 'pos1':pos[0],
            'name2':players[1], 'team2':team[1],'pos2':pos[1],
            'name3':players[2], 'team3':team[2], 'pos3':pos[2],
            'name4':players[3], 'team4':team[3], 'pos4':pos[3],
            'name5':players[4], 'team5':team[4], 'pos5':pos[4],
            'name6':players[5], 'team6':team[5], 'pos6':pos[5],
            'name7':players[6], 'team7':team[6], 'pos7':pos[6],
            'name8':players[7], 'team8':team[7], 'pos8':pos[7],
            'name9':players[8], 'team9':team[8], 'pos9':pos[8]})


if __name__== "__main__":
            basketball()
