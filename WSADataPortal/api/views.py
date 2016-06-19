from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import TimeKeeper, Rotowire, RotogrindersBatters
from api.serializers import TimeKeeperSerializer, RotowireSerializer, RotogrindersBattersSerializer
from bs4 import BeautifulSoup
from string import whitespace
import urllib2
import demjson
import json

# Create your views here.


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        logindata = request.data
        if logindata["password"] == 'H@tD00r!':
            return HttpResponse('You have the keys to the kingdom')
        else:
            return HttpResponseNotFound('You do not have the proper login')

#notes
# pull into database + then load?
# scrollable/clickable links to get you to table

@api_view(['GET'])
def baseballRotowireTimes(request):
    if request.method == 'GET':
        rotowireTimes = TimeKeeper.objects.filter(name='Rotowire Data')
        serializer = TimeKeeperSerializer(rotowireTimes, many=True)
        return HttpResponse(json.dumps(serializer.data))

@api_view(['GET'])
def baseballRotogrindersBattersTimes(request):
    if request.method == 'GET':
        rotogrindersBattersTimes = TimeKeeper.objects.filter(name='Rotogrinders Batters Data')
        serializer = TimeKeeperSerializer(rotogrindersBattersTimes, many=True)
        return HttpResponse(json.dumps(serializer.data))


@api_view(['POST', 'GET'])
def baseballRotowireData(request):
    if request.method == 'POST':
        if not request.data.items():
            # Rotowire Data
            url = "http://www.rotowire.com/daily/mlb/optimizer.htm?site=DraftKings&sport=MLB"

            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page, "html.parser")

            rotowireHeader = ['Name', 'Bats', 'Team', 'Position', 'Order in LU', 'Opponent',
                              'Opp Throws', 'Salary', 'Proj. Points', 'Ceiling', 'Floor', 'Value', 'M/L', 'O/U']

            rotoWireData = []

            RotowireEntry = TimeKeeper(name="Rotowire Data")
            RotowireEntry.save()

            for tr in soup.find_all('tr')[4:]:
                tds = tr.find_all('td')

                playerData = []

                # name
                playerInfo = tds[1]

                playerName = playerInfo.a
                playerName = playerName.text
                playerName = str(playerName.encode('utf-8'))
                playerData.append(playerName)

                playerStance = playerInfo.span

                if playerStance != None:
                    playerStance = playerStance.text
                    if playerStance == 'B':
                        playerStance = 'S'
                    if playerStance == 'DTD':
                        playerStance = "None"
                    playerStance = str(playerStance.encode('utf-8'))
                else:
                    playerStance = "None"
                    playerStance = str(playerStance.encode('utf-8'))

                playerData.append(playerStance)

                team = tds[2]['data-team']
                team = str(team.encode('utf-8'))
                playerData.append(team)

                position = tds[3].text
                position = str(position.encode('utf-8'))
                playerData.append(position)

                battingOrder = tds[4]['data-slot']
                battingOrder = str(battingOrder.encode('utf-8'))
                playerData.append(battingOrder)

                tds2 = tr.find_all('td', recursive=False)

                opponent = tds2[5].text
                opponent = opponent.replace('@', '')
                opponent = opponent.encode('ascii', 'ignore')
                opponent = opponent.translate(None, whitespace)
                opponent = opponent.replace("(L)", "")
                opponent = opponent.replace("(R)", "")
                opponent = str(opponent.encode('utf-8'))
                playerData.append(opponent)

                opponentData = tds[5]
                opponentThrowArm = opponentData.span
                if opponentThrowArm != None:
                    opponentThrowArm = opponentThrowArm.text
                    opponentThrowArm = opponentThrowArm.lstrip()
                    opponentThrowArm = opponentThrowArm.rstrip()
                    opponentThrowArm = str(opponentThrowArm.encode('utf-8'))
                else:
                    opponentThrowArm = "None"
                    opponentThrowArm = str(opponentThrowArm.encode('utf-8'))
                playerData.append(opponentThrowArm)

                salary = tds[6].text
                salary = str(salary[1:])
                salaries = salary.split(
                    ',')  # this must be created because some salaries are > 10,000 and some are 9,000 and below
                salary = str(salaries[0]) + str(salaries[1])  # FIXME
                playerData.append(salary)

                projpts = tds[7].text
                projpts = projpts.lstrip()
                projpts = projpts.rstrip()
                projpts = str(projpts.encode('utf-8'))
                if projpts == '':
                    projpts = tds[7]['data-points']
                    projpts = projpts.lstrip()
                    projpts = projpts.rstrip()
                    projpts = str(projpts.encode('utf-8'))
                playerData.append(projpts)

                ceiling = tds[7]['data-ceiling']
                ceiling = ceiling.lstrip()
                ceiling = ceiling.rstrip()
                ceiling = str(ceiling.encode('utf-8'))
                playerData.append(ceiling)

                floor = tds[7]['data-floor']
                floor = floor.lstrip()
                floor = floor.rstrip()
                floor = str(floor.encode('utf-8'))
                playerData.append(floor)

                value = tds[8].text
                value = value.lstrip()
                value = value.rstrip()
                value = str(value.encode('utf-8'))
                playerData.append(value)

                moneyLine = tds[9].text
                moneyLine = str(moneyLine.encode('utf-8'))
                playerData.append(moneyLine)

                overUnder = tds[10].text
                overUnder = str(overUnder.encode('utf-8'))
                playerData.append(overUnder)

                rotoWireData.append(playerData)

                playerEntry = Rotowire(parent=RotowireEntry, name=playerName, bats=playerStance, team=team, orderInLU=battingOrder,
                                       position=position, opponent=opponent, opponentThrows=opponentThrowArm,
                                       salary=salary,
                                       projPoints=projpts, ceiling=ceiling, floor=floor, value=value,
                                       moneyLine=moneyLine,
                                       overUnder=overUnder)
                playerEntry.save()

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotowireHeader:
                html += '<th>'
                html += header
                html += '</th>'

            for player in rotoWireData:
                html += '<tr>'
                for data in player:
                    html += '<td>'
                    html += data
                    html += '</td>'
                html += '</tr>'

            html += '</table>'

            return HttpResponse(html)

        else:
            rotoWireData = Rotowire.objects.filter(parent=request.data["id"])
            serializer = RotowireSerializer(rotoWireData, many=True)
            rotoWireSerializedData = serializer.data

            rotowireHeader = ['Name', 'Bats', 'Team', 'Position', 'Order in LU', 'Opponent',
                              'Opp Throws', 'Salary', 'Proj. Points', 'Ceiling', 'Floor', 'Value', 'M/L', 'O/U']

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotowireHeader:
                html += '<th>'
                html += header
                html += '</th>'

            for player in rotoWireSerializedData:
                html += '<tr>'
                for i, (key , value) in enumerate(player.iteritems()):
                    html += '<td>'
                    html += value
                    html += '</td>'
                html += '</tr>'

            html += '</table>'

            return HttpResponse(html)

@api_view(['POST', 'GET'])
def baseballRotogrindersBatterData(request):
    if request.method == 'POST':
        if not request.data.items():
            #rotogrindersBatters
            url = "https://rotogrinders.com/projected-stats/mlb-hitter?site=draftkings"

            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page, "html.parser")

            rotogrinderProjectionsHeader = ['Player Name', 'Position', 'Sec. Position', 'Salary', 'Team', 'Opp', 'Bats',
                                            'Ceiling', 'Floor', 'Projection', 'Value', 'Pitcher Name', 'Throws',
                                            'Season AB', 'Season Avg', 'Season wOBA', 'Season ISO', 'Season OBP',
                                            'Season BABIP', 'SLG %', 'K %', 'BB %', 'Season OPS']

            # get object
            script = soup.find_all("script")
            script = script[8].text

            # strip all junk
            scriptJunk, rotoObject = script.split("=")
            rotoObject, scriptJunk = rotoObject.split("projectedStats.init(data)")
            rotoObject = rotoObject.lstrip()
            rotoObject = rotoObject.rstrip()
            rotoObject = rotoObject[:-1]

            rotoProj = demjson.decode(rotoObject)

            RotogrindersBattersEntry = TimeKeeper(name='Rotogrinders Batters Data')
            RotogrindersBattersEntry.save()

            rotogrindersData = []

            for line in rotoProj:
                playerData = []

                playerName = ((line['player_name']))
                playerData.append(str(playerName))

                position = ((line['position']))

                secondaryPosition = ""
                if position.find('/') != -1:
                    position, secondaryPosition = position.split("/")

                playerData.append(str(position))
                playerData.append(str(secondaryPosition))

                salary = (line['salary'])
                playerData.append(str(salary))

                team = (line['team'])
                playerData.append(str(team))

                opponent = (line['opp'])
                playerData.append(str(opponent))

                playerHand = (line['player']['hand'])
                playerData.append(str(playerHand))

                ceil = (line['ceil'])
                playerData.append(str(ceil))

                floor = (line['floor'])
                playerData.append(str(floor))

                points = (line['points'])
                playerData.append(str(points))

                value = "None"
                playerData.append(str(value))

                pFirstName = (line['pitcher']['first_name'])
                pLastName = (line['pitcher']['last_name'])
                pitcherName = pFirstName + " " + pLastName
                playerData.append(str(pitcherName))

                pitcherHand = (line['pitcher']['hand'])
                playerData.append(str(pitcherHand))

                seasonAB = (line['ab'])
                playerData.append(str(seasonAB))

                avg = (line['avg'])
                playerData.append(str(avg))

                woba = (line['woba'])
                playerData.append(str(woba))

                iso = (line['iso'])
                playerData.append(str(iso))

                obp = (line['obp'])
                playerData.append(str(obp))

                babip = (line['babip'])
                playerData.append(str(babip))

                slg = (line['slg'])
                playerData.append(str(slg))

                kPercentage = (line['k%'])
                playerData.append(str(kPercentage))

                bb = (line['bb%'])
                playerData.append(str(bb))

                ops = (line['ops'])
                playerData.append(str(ops))

                rotogrindersData.append(playerData)

                RotogrindersBattersPlayerData = RotogrindersBatters(parent=RotogrindersBattersEntry, name=playerName, position=position,
                                                secondaryPosition=secondaryPosition, salary=salary, team=team, opponent=opponent,
                                                bats=playerHand, ceiling=ceil, floor=floor, projPoints=points, value=value,
                                                pitcherName=pitcherName, pitcherThrows=pitcherHand, seasonAB=seasonAB,
                                                average=avg, wOBA=woba, ISO=iso, OBP=obp, BABIP=babip, SLG=slg,
                                                kPercentage=kPercentage, BB=bb, OPS=ops)

                RotogrindersBattersPlayerData.save()

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotogrinderProjectionsHeader:
                html += '<th>'
                html += header
                html += '</th>'

            for player in rotogrindersData:
                html += '<tr>'
                for data in player:
                    html += '<td>'
                    html += data
                    html += '</td>'
                html += '</tr>'

            html += '</table>'

            return HttpResponse(html)

        else:
            rotogrindersBattersData = RotogrindersBatters.objects.filter(parent=request.data["id"])
            serializer = RotogrindersBattersSerializer(rotogrindersBattersData, many=True)
            rotogrindersBattersSerializedData = serializer.data

            rotogrinderProjectionsHeader = ['Player Name', 'Position', 'Sec. Position', 'Salary', 'Team', 'Opp', 'Bats',
                                            'Ceiling', 'Floor', 'Projection', 'Value', 'Pitcher Name', 'Throws',
                                            'Season AB', 'Season Avg', 'Season wOBA', 'Season ISO', 'Season OBP',
                                            'Season BABIP', 'SLG %', 'K %', 'BB %', 'Season OPS']

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotogrinderProjectionsHeader:
                html += '<th>'
                html += header
                html += '</th>'

            for player in rotogrindersBattersSerializedData:
                html += '<tr>'
                for i, (key , value) in enumerate(player.iteritems()):
                    html += '<td>'
                    if value is None:
                        html += "N/A"
                    else:
                        html += value
                    html += '</td>'
                html += '</tr>'

            html += '</table>'
            return HttpResponse(html)


@api_view(['POST', 'GET'])
def baseballRotogrindersPitcherData(request):
    if request.method == 'GET':
        url = "https://rotogrinders.com/projected-stats/mlb-pitcher?site=draftkings"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rotogrindersPitcherProjectionsHeader = ["Player Name", "Position", "Salary", "Team", "Opponent", "Player Hand",
                                                "Ceiling", "Floor", "Projection", "Value", "xISO", "xR", "xSLG",
                                                "xWOBA", "xL", "GP", "lWOBA", "rWOBA", "lSLG", "rSLG", "SIERA", "xFIP",
                                                "lISO", "rISO", "GBPercentage", "FBPercentage", "IP"]

        # get object
        script = soup.find_all("script")
        script = script[8].text

        # strip all junk
        scriptJunk, rotoObject = script.split("=")
        rotoObject, scriptJunk = rotoObject.split("projectedStats.init(data)")
        rotoObject = rotoObject.lstrip()
        rotoObject = rotoObject.rstrip()
        rotoObject = rotoObject[:-1]

        rotoProj = demjson.decode(rotoObject)

        rotogrindersPitcherData = []

        for line in rotoProj:
            playerData = []

            playerName = (line['player_name'])
            playerData.append(str(playerName))

            position = (line['position'])
            playerData.append(str(position))

            salary = (line['salary'])
            playerData.append(str(salary))

            team = (line['team'])
            playerData.append(str(team))

            opponent = (line['opp'])
            playerData.append(str(opponent))

            playerHand = (line['player']['hand'])
            playerData.append((str(playerHand)))

            ceil = (line['ceil'])
            playerData.append(str(ceil))

            floor = (line['floor'])
            playerData.append((str(floor)))

            points = (line['points'])
            playerData.append(str(points))

            value = "None"
            playerData.append(str(value))

            xIso = (line['xiso'])
            playerData.append(str(xIso))

            xR = (line['xr'])
            playerData.append(str(xR))

            xSLG = (line['xslg'])
            playerData.append(str(xSLG))

            xWOBA = (line['xwoba'])
            playerData.append(str(xWOBA))

            # xk9 = (line["xk\/9"])
            xl = (line['xl'])
            playerData.append(str(xl))

            gp = (line['gp'])
            playerData.append(str(gp))

            lwoba = (line['lwoba'])
            playerData.append(str(lwoba))

            rwoba = (line['rwoba'])
            playerData.append(str(rwoba))

            # lk9 = (line['lk\/9'])
            # rk9 = (line['rk\/9'])
            lSLG = (line['lslg'])
            playerData.append(str(lSLG))

            rSLG = (line['rslg'])
            playerData.append(str(rSLG))

            SIERA = (line['siera'])
            playerData.append(str(SIERA))

            xFIP = (line['xfip'])
            playerData.append(str(xFIP))

            # HRFB = (line['hr\/fb'])
            lISO = (line['liso'])
            playerData.append(str(lISO))

            rISO = (line['riso'])
            playerData.append(str(rISO))

            GBPercentage = (line['gb%'])
            playerData.append(str(GBPercentage))

            FBPercentage = (line['fb%'])
            playerData.append(str(FBPercentage))

            IP = (line['ip'])
            playerData.append(str(IP))

            rotogrindersPitcherData.append(playerData)

        html = '<table class="table table-hover table-bordered table-striped">'

        for header in rotogrindersPitcherProjectionsHeader:
            html += '<th>'
            html += header
            html += '</th>'

        for player in rotogrindersPitcherData:
            html += '<tr>'
            for data in player:
                html += '<td>'
                html += data
                html += '</td>'
            html += '</tr>'

        html += '</table>'

        return HttpResponse(html)

@api_view(['POST', 'GET'])
def baseballSwishAnalyticsBatterData(request):
    if request.method == 'GET':
        url = "https://www.swishanalytics.com/optimus/mlb/dfs-batter-projections"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        swishAnalyticsBatterProjectionsHeaders = ["Player Name", "Salary", "Bats", "Position", "Team", "Opponent",
                                                  "Projected Points", "Projected Value", "Outs", "AB", "Walks", "HBP",
                                                  "Singles", "Doubles", "Triples", "HR", "RBI", "SB", "CS",
                                                  "DraftKings Average"]

        script = soup.find_all("script")
        script = script[18].text

        # strip all junk
        scriptJunk, rotoObject = script.split("this.batterArray")
        rotoObject, scriptJunk = rotoObject.split("this.updatedBatterArray")
        rotoObject = rotoObject[2:]
        rotoObject = rotoObject.lstrip()
        rotoObject = rotoObject.rstrip()
        rotoObject = rotoObject[:-1]

        rotoProj = demjson.decode(rotoObject)

        swishAnalyticsBatterData = []

        for line in rotoProj:
            playerData = []

            playerName = (line['player_name'])
            playerData.append(str(playerName))

            salary = (line['dk_salary'])
            salary = salary.replace(",", "")
            playerData.append(str(salary))

            bats = (line['bats'])
            playerData.append(str(bats))

            dk_pos = (line['dk_pos'])
            playerData.append(str(dk_pos))

            team = (line['team_short'])
            playerData.append(str(team))

            opponent = (line['matchup'])
            opponent = opponent.replace("vs", "")
            opponent = opponent.replace("@", "")
            opponent = opponent.lstrip()
            playerData.append(str(opponent))

            projPts = (line['dk_pts'])
            playerData.append(str(projPts))

            projValue = (line['dk_value'])
            playerData.append(str(projValue))

            outs = (line['outs'])
            playerData.append(str(outs))

            ab = (line['ab'])
            playerData.append(str(ab))

            bb = (line['bb'])
            playerData.append(str(bb))

            hbp = (line['hbp'])
            playerData.append(str(hbp))

            singles = (line['singles'])
            playerData.append(str(singles))

            doubles = (line['doubles'])
            playerData.append(str(doubles))

            triples = (line['triples'])
            playerData.append(str(triples))

            hr = (line['hr'])
            playerData.append(str(hr))

            rbi = (line['rbi'])
            playerData.append(str(rbi))

            sb = (line['sb'])
            playerData.append(str(sb))

            cs = (line['cs'])
            playerData.append(str(cs))

            dk_avg = (line['dk_avg'])
            playerData.append(str(dk_avg))

            swishAnalyticsBatterData.append(playerData)

        html = '<table class="table table-hover table-bordered table-striped">'

        for header in swishAnalyticsBatterProjectionsHeaders:
            html += '<th>'
            html += header
            html += '</th>'

        for player in swishAnalyticsBatterData:
            html += '<tr>'
            for data in player:
                html += '<td>'
                html += data
                html += '</td>'
            html += '</tr>'

        html += '</table>'

        return HttpResponse(html)

@api_view(['POST', 'GET'])
def baseballSwishAnalyticsPitcherData(request):
    if request.method == 'GET':
        url = "https://www.swishanalytics.com/optimus/mlb/dfs-pitcher-projections"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        swishAnalyticsPitcherProjectionsHeaders = ["Player Name", "Salary", "Team", "Opponent", "Proj. Points",
                                                   "Proj. Value", "Outs", "ER", "H", "BB", "HBP",
                                                   "K", "CG Probability", "CGSO Probability", "No Hit Probability",
                                                   "W Probability", "DraftKings Average"]

        script = soup.find_all("script")
        script = script[20].text

        # strip all junk
        scriptJunk, rotoObject = script.split("this.pitcherArray")
        rotoObject, scriptJunk = rotoObject.split("this.updatedpitcherArray")
        rotoObject = rotoObject[2:]
        rotoObject = rotoObject.lstrip()
        rotoObject = rotoObject.rstrip()
        rotoObject = rotoObject[:-1]

        rotoProj = demjson.decode(rotoObject)

        swishAnalyticsPitcherData = []

        for line in rotoProj:
            playerData = []

            playerName = (line['player_name'])
            playerData.append(playerName)

            salary = (line['dk_salary'])
            salary = salary.replace(",", "")
            playerData.append(salary)

            team = (line['team_short'])
            playerData.append(team)

            opponent = (line['matchup'])
            opponent = opponent.replace("vs", "")
            opponent = opponent.replace("@", "")
            opponent = opponent.lstrip()
            playerData.append(opponent)

            projPts = (line['dk_pts'])
            playerData.append(projPts)

            projValue = (line['dk_value'])
            playerData.append(projValue)

            outs = (line['outs'])
            playerData.append(outs)

            ER = (line['er'])
            playerData.append(ER)

            hits = (line['h'])
            playerData.append(hits)

            walks = (line['bb'])
            playerData.append(walks)

            hbp = (line['hbp'])
            playerData.append(hbp)

            strikeouts = (line['so'])
            playerData.append(strikeouts)

            completeGame = (line['cg'])
            playerData.append(completeGame)

            completeGameSO = (line['cgso'])
            playerData.append(completeGameSO)

            noHit = (line['noh'])
            playerData.append(noHit)

            win = (line['win'])
            playerData.append(win)

            dk_avg = (line['dk_avg'])
            playerData.append(dk_avg)

            swishAnalyticsPitcherData.append(playerData)

        html = '<table class="table table-hover table-bordered table-striped">'

        for header in swishAnalyticsPitcherProjectionsHeaders:
            html += '<th>'
            html += header
            html += '</th>'

        for player in swishAnalyticsPitcherData:
            html += '<tr>'
            for data in player:
                html += '<td>'
                html += data
                html += '</td>'
            html += '</tr>'

        html += '</table>'

        return HttpResponse(html)
