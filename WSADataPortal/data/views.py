from django.shortcuts import HttpResponse, render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse



# Create your views here.

def index(request):
	return render(request, 'data/index.html')

def home(request):
	return render(request, 'data/home.html')

def baseball(request):
	return render(request, 'data/baseball.html')

def uploadBaseball(request):
	return render(request, 'data/baseballupload.html')