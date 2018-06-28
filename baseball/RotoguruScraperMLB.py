import requests
import csv
from bs4 import BeautifulSoup, Comment
from pydfs_lineup_optimizer import * # version >= 2.0.1

'''
Fanduel Scraper that scrapes rotogur for predicitions and optimizes lineups in place
'''
def predict():
    url = "https://rotogrinders.com/projected-stats/mlb-pitcher.csv?site=fanduel"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    player_list = []

    for row in str(soup).split('\n')[:-1]:
        rows = row.split(",")
        names = rows[0][1:-1].split()
        pos = rows[3]
        team = rows[2]
        sal = rows[1]
        rotoProj = rows[7]

        player_list.append(Player(0, names[0], names[1], pos, team, float(sal), float(rotoProj), False))

    url = "https://rotogrinders.com/projected-stats/mlb-hitter.csv?site=fanduel"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for row in str(soup).split('\n')[:-1]:
        rows = row.split(",")
        names = rows[0][1:-1].split()
        pos = rows[3]
        if pos == "C-1B":
            pos = ["C", "1B"]
        else:
            pos = [pos]
        team = rows[2]
        sal = rows[1]
        rotoProj = rows[7]

        player_list.append(Player(0, names[0], names[1], pos, team, float(sal), float(rotoProj), False))

    optimizer = get_optimizer(Site.FANDUEL, Sport.BASEBALL)
    optimizer.load_players(player_list)

    numLineups = 5

    lineups = optimizer.optimize(n=numLineups, max_exposure=0.3)

    return lineups

if __name__ == "__main__":

    predict()
