from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'baseball/baseball.html')

def lineups(request):
    context = []
    return render(request, 'baseball/lineups.html', context)
