from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from get_tree import get_rankings

# Create your views here.
def tree(request):
    rankings = get_rankings()

    return render(request, 'ncaa/tree.html', context={"rankings":rankings} )
