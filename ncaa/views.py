from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from get_tree import get_rankings
from django.core.cache import cache
from threading import Thread


# Create your views here.
def tree(request):

    rankings = cache.get('TreeRankings')
    if not rankings:
        thread = Thread(target=set_rankings_cache)
        thread.start()

    return render(request, 'ncaa/tree.html', context={"rankings":rankings} )


def set_rankings_cache():
    rankings = get_rankings()
    cache.set('TreeRankings', rankings, (6*60*60))
