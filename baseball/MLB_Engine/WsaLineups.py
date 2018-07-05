'''
 Wsa Lineup object that holds one baseball lineup
 Requeres players, date, time that lineup can be played before and projected points
'''
class WsaLineup():
    def __init__(self, players, date, slate, points, op_type):
        self.pitcher = players[0]
        self.c_or_1B = players[1]
        self.P2B = players[2]
        self.P3B = players[3]
        self.SS = players[4]
        self.OF1 = players[5]
        self.OF2 = players[6]
        self.OF3 = players[7]
        self.UTIL = players[8]
        self.slate = slate
        self.date = date
        self.points = points
        self.op_type = op_type

    # insert each lineup with corresponding number into table
    def insertTable(self, cursor, lineupNumber):

        query = "Replace into lineups (lineupNumber, date, P, C1B, 2B, 3B, SS, OF1, OF2, OF3, UTIL, slateName, projectedPoints, lineupType) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        inserts = (lineupNumber, self.date, self.pitcher, self.c_or_1B, self.P2B, self.P3B, self.SS, self.OF1, self.OF2, self.OF3, self.UTIL, self.slate, self.points, self.op_type)
        cursor.execute(query, inserts)
