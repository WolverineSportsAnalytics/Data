from django.shortcuts import HttpResponse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
import random
import string


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

       
        return render(request, 'data/basket.html',  context={'name1':id_generator(), 'team1':'CHI', 'pos1':"PF",
            'name2':id_generator(), 'team2':'SAS', 'pos2':"PG",
            'name3':id_generator(), 'team3':'HOU', 'pos3':"SF",
            'name4':id_generator(), 'team4':'OKC', 'pos4':"PF",
            'name5':id_generator(), 'team5':'DET', 'pos5':"SG",
            'name6':id_generator(), 'team6':'GSW', 'pos6':"SF",
            'name7':id_generator(), 'team7':'BOS', 'pos7':"SG",
            'name8':id_generator(), 'team8':'LAL', 'pos8':"PG",
            'name9':id_generator(), 'team9':'NYK', 'pos9':"C"})

