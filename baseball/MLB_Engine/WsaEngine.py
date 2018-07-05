import RotoGuruScraperMLB as rgs
import RotoWireScraper as rws
import MlbOptimizer 
import mysql.connector
import datetime
from selenium import webdriver
import WsaLineups
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, Comment
import time

teamMap = {"CHW":"CWS", "TBR":"TB", "SDP":"SD", "KCR":"KC", "SFG":"SF"}


class Slate():
    def __init__(self, teams, name):
        self.teams = teams
        self.name = name


class WsaEngine():
    def __init__(self):
        self.rgsHitters = rgs.RotoGuruScraper("https://rotogrinders.com/projected-stats/mlb-hitter.csv?site=fanduel")
        self.rgsPitchers = rgs.RotoGuruScraper("https://rotogrinders.com/projected-stats/mlb-pitcher.csv?site=fanduel")
        self.rws = rws.RotoScraper( "https://www.rotowire.com/daily/mlb/optimizer.php?site=FanDuel&sport=mlb")
        
    def get_slates(self):
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        browser = webdriver.Chrome(executable_path=("./chromedriver"),   chrome_options=chrome_options)
        
        url = "https://rotogrinders.com/lineuphq/mlb?site=fanduel"
        browser.get(url) #navigate to the page
        browser.find_element_by_id("slate-menu-link").click()
        time.sleep(3)
        page =browser.find_element_by_id("slate-select-menu").get_attribute("innerHTML")
        soup = BeautifulSoup(page, "html.parser")
        slates = soup.find_all("li",{"class": "slate-menu__slate"})
        
        slate_list = []
        for slate in slates:
            name = slate.find_all("b",{"class": "slate-menu__label"})[0].find("span").text
            games = slate.find_all("li",{"class": "slate-menu__game"})
            teams = []
            for game in games:
                split = game.find("span").text.split()
                if split[0] in teamMap:
                    teams.append(teamMap[split[0]])
                else:
                    teams.append(split[0])
                if split[2] in teamMap:
                    teams.append(teamMap[split[2]])
                else:
                    teams.append(split[2])

            slate_list.append(Slate(teams, name))
        
        browser.quit()
        self.slates = slate_list

    def setLineups(self, cursor, cnx, date):
        scrapers = [self.rws, self.rgsHitters, self.rgsPitchers]
        for scraper in scrapers:
            scraper.get_soup() # go get the text 
            for player in scraper.get_players(): # parse out the players
                player.insertTable(cursor, date) # insert all the players

        
        cursor.execute("Delete from players where RotoWireProjection is null")
        
        cnx.commit()
         

        opt = MlbOptimizer.MlbOptimizer(date, cursor)
        opt.getPlayers(date)

        for slate in self.slates:
            opt.generateLineups("rotowire", 1, date, time, slate)
            opt.insertLineups(cursor)
            opt.generateLineups("rotoGrinders", 1, date, time, slate)
            opt.insertLineups(cursor)
            opt.generateLineups("average", 1, date, time, slate)
            opt.insertLineups(cursor)

    # gets lineups for that are closest to a specific time
    def getLineups(self, cursor, date, slate):
         
        query = "Select * from lineups where date=%s and slateName=%s"
        cursor.execute(query, (date, closestStart))
        fetchedLineups = cursor.fetchall()
        lineups = []
        for line in fetchedLineups:
            lineups.append(WsaLineups.WsaLineup(line[2:11], line[1], line[11], line[12], line[13]))

        return lineups

    # get all lineups for a day
    def getAllLineups(self, cursor, date):

        query = "Select * from lineups where date=%s"
        cursor.execute(query, (date,) )
        fetchedLineups = cursor.fetchall()
        lineups = []
        for line in fetchedLineups:
            lineups.append(WsaLineups.WsaLineup(line[2:11], line[1], line[11], line[12], line[13]))

        return lineups

        

def genMlbLineups():
        cnx = mysql.connector.connect(user="root",
                host="127.0.0.1",
                database="mlb",
                password="")                                                                                                               
        cursor = cnx.cursor()
        
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.now().strftime('%H:%M:%S')

        gen = WsaEngine()
        gen.get_slates()
        gen.setLineups(cursor,cnx, today)

        cnx.commit()

if __name__=="__main__":
    genMlbLineups()
