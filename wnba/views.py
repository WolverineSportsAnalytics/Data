from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'wnba/index.html')

def lineups(request):
    context = []
    return render(request, 'wnba/lineups.html', context)
