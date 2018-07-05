import requests
from bs4 import BeautifulSoup, Comment
from pydfs_lineup_optimizer import * # version >= 2.0.1
import datetime
from pytz import timezone
from WsaPlayer import WsaPlayer

'''
Fanduel Scraper that scrapes rotoWire for predicitions and returns a WsaPlayer list
'''

class RotoScraper():
    def __init__(self, url):
        self.url = url
        self.players = []
        self.gameTimes = {}
        self.startTimes = []

    # Returns Dictionary of key:team value:starttime as well as a set of all start times
    def get_game_times(self):
        games = self.soup.find("div",{"id":"rwo-matchups"}).find_all("div",{"class":"rwo-game-team"})
        zone = timezone("US/Eastern")
        now = datetime.datetime.now(tz=zone).time().strftime('%H:%M:%S')
        for game in games:
            team = game['data-team']
            time = game['data-gametimeonly']
            self.gameTimes[team] = time
            self.startTimes.append(time)

        return self.gameTimes, set(self.startTimes)
    
    def get_soup(self):
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.text, "html.parser")

    def get_players(self):
        playersSoup = self.soup.find_all('tr')
        for i,count in zip(playersSoup[4:],range(len(playersSoup)-4)):
            try:
                name  = i.find_all('td')[1].text # name 
                names = name.split()
                name = names[0] + ' ' + names[1]
                
                
                team  = i.find_all('td')[2].text.rstrip()# team

                pos = i.find_all('td')[3].text # pos
                if pos == 'C1':
                    pos = ['1B','C']
                else:
                    pos = [str(pos)]
                sal = i.find_all('td')[6].find('input')['value']
                sal = sal[1:]
                sals = sal.split(",")
                sal = sals[0] + sals[1]
                rotoProj = i.find_all('td')[7].find('input')['value']
                self.players.append(WsaPlayer(name, sal, team, pos, rotoProj, None))

            except Exception as e:
                print e

        return self.players
