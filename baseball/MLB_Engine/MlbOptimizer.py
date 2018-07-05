from pydfs_lineup_optimizer import * # version >= 2.0.1
import datetime
import WsaLineups

''' Object that with optimize and insert lineups into database 
    Takes a database connection cursor and date as paremeters 
    Requires that the playes table has been prepopulated     '''
class MlbOptimizer():
    def __init__(self, date, cursor):
        self.cursor = cursor
        self.getPlayers(date)
        self.my_lineups = []
    
    def getPlayers(self, date):
        query = "Select * from players where date=\"" + date + "\""

        self.cursor.execute(query)
        self.players = self.cursor.fetchall()

    def generateLineups(self, op_type, numLineups, date, time, slate):
        opt_players = []
        count = 0
        for player in self.players:
            if player[3] in slate.teams: 
                # if proj is null
                if player[6] is None:
                    proj = player[5]
                elif op_type =="rotowire":
                    proj = player[5]
                elif op_type =="rotoGrinders":
                    proj = player[6]
                elif op_type =="average":
                    proj = (float(player[5]) + float(player[6]))/float(2.0)
                
                opt_players.append(Player(count,player[1], "", player[2].split("/"), player[3], float(player[4]), float(proj), False))
                count+=1


        optimizer = get_optimizer(Site.FANDUEL, Sport.BASEBALL)
        optimizer.load_players(opt_players)

        lineups = optimizer.optimize(n=numLineups, max_exposure=0.3)
        for lineup in lineups:
            sublineup = []
            for player in lineup.players:
                sublineup.append(player.first_name)
            points = lineup.fantasy_points_projection
            self.my_lineups.append(WsaLineups.WsaLineup(sublineup, date, slate.name, points, op_type))

    def insertLineups(self, cursor):
        count = 1 
        for lineup in self.my_lineups:
            lineup.insertTable(cursor, count)
            count += 1
        self.my_lineups = []



