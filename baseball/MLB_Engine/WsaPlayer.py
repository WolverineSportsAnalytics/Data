# WSA player object that can be inserted into table
class WsaPlayer():
    def __init__(self, name, sal, team, pos, WireProj, GrinderProj):
        self.name = name
        self.sal = sal
        self.team = team
        self.pos = "/".join(pos)
        self.WireProj = WireProj
        self.GrinderProj = GrinderProj

    def insertTable(self, cursor, date):
        
        query = "Insert into players (date, name, position, team, salary, RotoWireProjection, RotoGrindersProjection) values(%s, %s, %s, %s, %s, %s, %s) on duplicate key update" 

        if self.WireProj is None:
            query += " RotoGrindersProjection=%s"
            inserts = (date, self.name, self.pos, self.team, int(self.sal), self.WireProj, self.GrinderProj, self.GrinderProj)
        elif self.GrinderProj is None:
            inserts = (date, self.name, self.pos, self.team, int(self.sal), self.WireProj, self.GrinderProj, self.WireProj, self.team)
            query += " RotoWireProjection=%s, team=%s"

        cursor.execute(query, inserts)
