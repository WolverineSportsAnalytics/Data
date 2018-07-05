import requests
from bs4 import BeautifulSoup, Comment
from WsaPlayer import WsaPlayer 

'''
Fanduel Scraper that scrapes rotoGrinders for predicitions and returns a WsaPlayer Object
'''
class RotoGuruScraper():
    def __init__(self, url):
        self.url = url
        self.players = []
        self.finished_games = []
       
    def get_soup(self):
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.text, "html.parser")

    def get_players(self):
        for row in str(self.soup).split('\n')[:-1]:
            rows = row.split(",")
            names = rows[0][1:-1].split()
            pos = rows[3]
            team = rows[2]
            sal = rows[1]
            rotoProj = rows[7]

            self.players.append(WsaPlayer(names[0] + " " + names[1], sal, team, pos, None, rotoProj))
        return self.players
