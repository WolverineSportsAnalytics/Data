from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import TimeKeeper, Rotowire, RotogrindersBatters, RotogrindersPitchers, SwishAnalyticsBatters, \
    SwishAnalyticsPitchers, PitcherLeftSplits, PitcherRightSplits
from api.serializers import TimeKeeperSerializer, RotowireSerializer, RotogrindersBattersSerializer, \
    RotogrindersPitchersSerializer, SwishAnalyticsBattersSerializer, SwishAnalyticsPitchersSerializer, \
    PitcherLeftSplitsSerializer, PitcherRightSplitsSerializer
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

@api_view(['GET'])
def baseballRotogrindersPitchersTimes(request):
    if request.method == 'GET':
        rotogrindersPitchersTimes = TimeKeeper.objects.filter(name='Rotogrinders Pitchers Data')
        serializer = TimeKeeperSerializer(rotogrindersPitchersTimes, many=True)
        return HttpResponse(json.dumps(serializer.data))

@api_view(['GET'])
def baseballSwishAnalyticsBattersTimes(request):
    if request.method == 'GET':
        swishAnalyticsBattersTimes = TimeKeeper.objects.filter(name='Swish Analytics Batters Data')
        serializer = TimeKeeperSerializer(swishAnalyticsBattersTimes, many=True)
        return HttpResponse(json.dumps(serializer.data))

@api_view(['GET'])
def baseballSwishAnalyticsPitchersTimes(request):
    if request.method == 'GET':
        swishAnalyticsPitchersTimes = TimeKeeper.objects.filter(name='Swish Analytics Pitcher Data')
        serializer = TimeKeeperSerializer(swishAnalyticsPitchersTimes, many=True)
        return HttpResponse(json.dumps(serializer.data))

@api_view(['GET'])
def baseballPitcherLeftHandSplitsTimes(request):
    if request.method == 'GET':
        swishAnalyticsPitchersTimes = TimeKeeper.objects.filter(name='Rotogrinders Left Hand Pitcher Splits Data')
        serializer = TimeKeeperSerializer(swishAnalyticsPitchersTimes, many=True)
        return HttpResponse(json.dumps(serializer.data))

@api_view(['GET'])
def baseballPitcherRightHandSplitsTimes(request):
    if request.method == 'GET':
        swishAnalyticsPitchersTimes = TimeKeeper.objects.filter(name='Rotogrinders Right Hand Pitcher Splits Data')
        serializer = TimeKeeperSerializer(swishAnalyticsPitchersTimes, many=True)
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
            script = script[11].text

            # strip all junk
            scriptJunk, rotoObject = script.split("=")
            rotoObject, scriptJunk = rotoObject.split("projectedStats.init(data")
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
                pitcherName = ""
                if (pFirstName is None):
                    pitcherName = pLastName
                elif pLastName is None:
                    pitcherName = pFirstName
                else:
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
    if request.method == 'POST':
        if not request.data.items():
            url = "https://rotogrinders.com/projected-stats/mlb-pitcher?site=draftkings"

            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page, "html.parser")

            rotogrindersPitcherProjectionsHeader = ["Player Name", "Position", "Salary", "Team", "Opponent", "Player Hand",
                                                    "Ceiling", "Floor", "Projection", "Value", "xISO", "xR", "xSLG",
                                                    "xWOBA", "xL", "GP", "lWOBA", "rWOBA", "lSLG", "rSLG", "SIERA", "xFIP",
                                                    "lISO", "rISO", "GBPercentage", "FBPercentage", "IP"]

            # get object
            script = soup.find_all("script")
            script = script[11].text

            # strip all junk
            scriptJunk, rotoObject = script.split("=")
            rotoObject, scriptJunk = rotoObject.split("projectedStats.init(data")
            rotoObject = rotoObject.lstrip()
            rotoObject = rotoObject.rstrip()
            rotoObject = rotoObject[:-1]

            rotoProj = demjson.decode(rotoObject)

            RotogrindersPitchersEntry = TimeKeeper(name='Rotogrinders Pitchers Data')
            RotogrindersPitchersEntry.save()

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

                rotogrindersPitcherEntry = RotogrindersPitchers(parent=RotogrindersPitchersEntry,
                                                                name=playerName, position=position, salary=salary,
                                                                team=team, opponent=opponent, playerThrows=playerHand,
                                                                ceiling=ceil, floor=floor, projPoints=points, value=value,
                                                                xISO=xIso, xR=xR, xSLG=xSLG, xWOBA=xWOBA, xL=xl, GP=gp,
                                                                lWOBA=lwoba, rWOBA=rwoba, lSLG=lSLG, rSLG=rSLG, SIERA=SIERA,
                                                                xFIP=xFIP, lISO=rISO, GBPercentage=GBPercentage,
                                                                FBPercentage=FBPercentage, IP=IP)
                rotogrindersPitcherEntry.save()

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

        else:
            rotogrindersPitchersData = RotogrindersPitchers.objects.filter(parent=request.data["id"])
            serializer = RotogrindersPitchersSerializer(rotogrindersPitchersData, many=True)
            rotogrindersPitchersSerializedData = serializer.data

            rotogrindersPitcherProjectionsHeader = ["Player Name", "Position", "Salary", "Team", "Opponent",
                                                    "Player Hand",
                                                    "Ceiling", "Floor", "Projection", "Value", "xISO", "xR", "xSLG",
                                                    "xWOBA", "xL", "GP", "lWOBA", "rWOBA", "lSLG", "rSLG", "SIERA",
                                                    "xFIP",
                                                    "lISO", "rISO", "GBPercentage", "FBPercentage", "IP"]

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotogrindersPitcherProjectionsHeader:
                html += '<th>'
                html += header
                html += '</th>'

            for player in rotogrindersPitchersSerializedData:
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
def baseballSwishAnalyticsBatterData(request):
    if request.method == 'POST':
        if not request.data.items():
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

            swishAnalyticsBattersTimeEntry = TimeKeeper(name='Swish Analytics Batters Data')
            swishAnalyticsBattersTimeEntry.save()

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

                swishAnalyticsBatterEntry = SwishAnalyticsBatters(parent=swishAnalyticsBattersTimeEntry, name=playerName,
                                                                  salary=salary, bats=bats, position=dk_avg, opponent=opponent,
                                                                  projPoints=projPts, value=projValue, outs=outs, AB=ab,
                                                                  BB=bb, HBP=hbp, singles=singles, doubles=doubles,
                                                                  triples=triples, HR=hr, RBI=rbi, SB=sb, CS=cs,
                                                                  averageDKPoints=dk_avg)
                swishAnalyticsBatterEntry.save()

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

        else:
            swishAnalyticsBattersData = SwishAnalyticsBatters.objects.filter(parent=request.data["id"])
            serializer = SwishAnalyticsBattersSerializer(swishAnalyticsBattersData, many=True)
            swishAnalyticsBattersSerializedData = serializer.data

            swishAnalyticsBatterProjectionsHeaders = ["Player Name", "Salary", "Bats", "Position", "Team", "Opponent",
                                                      "Projected Points", "Projected Value", "Outs", "AB", "Walks",
                                                      "HBP",
                                                      "Singles", "Doubles", "Triples", "HR", "RBI", "SB", "CS",
                                                      "DraftKings Average"]

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in swishAnalyticsBatterProjectionsHeaders:
                html += '<th>'
                html += header
                html += '</th>'

            for player in swishAnalyticsBattersSerializedData:
                html += '<tr>'
                for i, (key, value) in enumerate(player.iteritems()):
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
def baseballSwishAnalyticsPitcherData(request):
    if request.method == 'POST':
        if not request.data.items():
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

            swishAnalyticsPitchersTimeEntry = TimeKeeper(name='Swish Analytics Pitcher Data')
            swishAnalyticsPitchersTimeEntry.save()

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

                swishAnalyticsPitcherEntry = SwishAnalyticsPitchers(parent=swishAnalyticsPitchersTimeEntry,
                                                                    averageDKPoints=dk_avg, CG=completeGame, CGSO=completeGameSO,
                                                                    ER=ER, HBP=hbp, Hits=hits, Ks=strikeouts, NOHit=noHit,
                                                                    name=playerName, opponent=opponent, outs=outs,
                                                                    projPoints=projPts, salary=salary, team=team,
                                                                    value=projValue, Walks=walks, Win=win)
                swishAnalyticsPitcherEntry.save()

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

        else:
            swishAnalyticsPitchersData = SwishAnalyticsPitchers.objects.filter(parent=request.data["id"])
            serializer = SwishAnalyticsPitchersSerializer(swishAnalyticsPitchersData, many=True)
            swishAnalyticsSerializedPitchersData = serializer.data

            swishAnalyticsPitcherProjectionsHeaders = ["Player Name", "Salary", "Team", "Opponent", "Proj. Points",
                                                       "Proj. Value", "Outs", "ER", "H", "BB", "HBP",
                                                       "K", "CG Probability", "CGSO Probability", "No Hit Probability",
                                                       "W Probability", "DraftKings Average"]

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in swishAnalyticsPitcherProjectionsHeaders:
                html += '<th>'
                html += header
                html += '</th>'

            for player in swishAnalyticsSerializedPitchersData:
                html += '<tr>'
                for i, (key, value) in enumerate(player.iteritems()):
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
def baseballRotogrindersRightHandedPitcherSplits(request):
    if request.method == 'POST':
        if not request.data.items():
            url = "https://rotogrinders.com/pages/starting-pitcher-splits-335278"

            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page, "html.parser")

            rotogrindersPitcherSplitsHeaders = ["Name", "Team", "Opponent", "IP", "AVG", "wOBA", "OPS", "K/9", "BABIP", "BB%",
                                                "WHIP", "ERA", "FIP", "LOB%", "FB%", "HR/FB"]

            rotogrindersPitcherRSplitsData = []

            RotogrindersPitcherRSplitsEntry = TimeKeeper(name="Rotogrinders Right Hand Pitcher Splits Data")
            RotogrindersPitcherRSplitsEntry.save()

            rSplitsTable = soup.find_all('tbody')[1]

            for tr in rSplitsTable.find_all('tr'):
                tds = tr.find_all('td')

                playerData = []

                playerName = tds[0].a
                if playerName is None:
                    playerName = tds[0]
                playerName = playerName.text
                playerName = playerName.strip()
                playerData.append(playerName)

                team = tds[1].span
                team = team.text
                team = team.strip()
                playerData.append(team)

                opponent = tds[2].span
                opponent = opponent.text
                opponent = opponent.strip()
                playerData.append(opponent)

                inningsPitched = tds[3].text
                inningsPitched = inningsPitched.lstrip()
                inningsPitched = inningsPitched.rstrip()
                playerData.append(inningsPitched)

                average = tds[4].text
                average = average.lstrip()
                average = average.rstrip()
                playerData.append(average)

                wOBA = tds[5].text
                wOBA = wOBA.lstrip()
                wOBA = wOBA.rstrip()
                playerData.append(wOBA)

                OPS = tds[6].text
                OPS = OPS.lstrip()
                OPS = OPS.rstrip()
                playerData.append(OPS)

                k9 = tds[7].text
                k9 = k9.strip()
                playerData.append(k9)

                babip = tds[8].text
                babip = babip.strip()
                playerData.append(babip)

                bbPercentage = tds[9].text
                bbPercentage = bbPercentage.strip()
                playerData.append(bbPercentage)

                WHIP = tds[10].text
                WHIP = WHIP.strip()
                playerData.append(WHIP)

                ERA = tds[11].text
                ERA = ERA.strip()
                playerData.append(ERA)

                FIP = tds[12].text
                FIP = FIP.strip()
                playerData.append(FIP)

                leftOnBase = tds[13].text
                leftOnBase = leftOnBase.strip()
                playerData.append(leftOnBase)

                fbPercentage = tds[14].text
                fbPercentage = fbPercentage.strip()
                playerData.append(fbPercentage)

                hrFB = tds[15].text
                hrFB = hrFB.strip()
                playerData.append(hrFB)

                rotogrindersPitcherRSplitsData.append(playerData)

                pitchersRightSplitsEntry = PitcherRightSplits(parent=RotogrindersPitcherRSplitsEntry, name=playerName,
                                                            team=team, opponent=opponent,
                                                            avg=average, babip=babip, ip=inningsPitched, woba=wOBA,
                                                            knine=k9, bbPercentage=bbPercentage, whip=WHIP, era=ERA,
                                                            fip=FIP,
                                                            lob=leftOnBase, fb=fbPercentage, hrfb=hrFB, ops=OPS)
                pitchersRightSplitsEntry.save()

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotogrindersPitcherSplitsHeaders:
                html += '<th>'
                html += header
                html += '</th>'

            for player in rotogrindersPitcherRSplitsData:
                html += '<tr>'
                for data in player:
                    html += '<td>'
                    html += data
                    html += '</td>'
                html += '</tr>'

            html += '</table>'

            return HttpResponse(html)

        else:
            pitcherSplitsRightData = PitcherRightSplits.objects.filter(parent=request.data["id"])
            serializer = PitcherRightSplitsSerializer(pitcherSplitsRightData, many=True)
            pitcherRightSplitsSerializedData = serializer.data

            rotogrindersPitcherSplitsHeaders = ["Name", "Team", "Opponent", "IP", "AVG", "wOBA", "OPS", "K/9", "BABIP",
                                                "BB%",
                                                "WHIP", "ERA", "FIP", "LOB%", "FB%", "HR/FB"]

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotogrindersPitcherSplitsHeaders:
                html += '<th>'
                html += header
                html += '</th>'

            for player in pitcherRightSplitsSerializedData:
                html += '<tr>'
                for i, (key, value) in enumerate(player.iteritems()):
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
def baseballRotogrindersLeftHandedPitcherSplits(request):
    if request.method == 'POST':
        if not request.data.items():
            url = "https://rotogrinders.com/pages/starting-pitcher-splits-335278"

            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page, "html.parser")

            rotogrindersPitcherSplitsHeaders = ["Name", "Team", "Opponent", "IP", "AVG", "wOBA", "OPS", "K/9", "BABIP", "BB%",
                                                "WHIP", "ERA", "FIP", "LOB%", "FB%", "HR/FB"]

            rotogrindersPitcherLSplitsData = []

            RotogrindersPitcherLSplitsEntry = TimeKeeper(name="Rotogrinders Left Hand Pitcher Splits Data")
            RotogrindersPitcherLSplitsEntry.save()

            lSplitsTable = soup.find_all('tbody')[2]

            for tr in lSplitsTable.find_all('tr'):
                tds = tr.find_all('td')

                playerData = []

                playerName = tds[0].a
                if playerName is None:
                    playerName = tds[0]
                playerName = playerName.text
                playerName = playerName.strip()
                playerData.append(playerName)

                team = tds[1].span
                team = team.text
                team = team.strip()
                playerData.append(team)

                opponent = tds[2].span
                opponent = opponent.text
                opponent = opponent.strip()
                playerData.append(opponent)

                inningsPitched = tds[3].text
                inningsPitched = inningsPitched.lstrip()
                inningsPitched = inningsPitched.rstrip()
                playerData.append(inningsPitched)

                average = tds[4].text
                average = average.lstrip()
                average = average.rstrip()
                playerData.append(average)

                wOBA = tds[5].text
                wOBA = wOBA.lstrip()
                wOBA = wOBA.rstrip()
                playerData.append(wOBA)

                OPS = tds[6].text
                OPS = OPS.lstrip()
                OPS = OPS.rstrip()
                playerData.append(OPS)

                k9 = tds[7].text
                k9 = k9.strip()
                playerData.append(k9)

                babip = tds[8].text
                babip = babip.strip()
                playerData.append(babip)

                bbPercentage = tds[9].text
                bbPercentage = bbPercentage.strip()
                playerData.append(bbPercentage)

                WHIP = tds[10].text
                WHIP = WHIP.strip()
                playerData.append(WHIP)

                ERA = tds[11].text
                ERA = ERA.strip()
                playerData.append(ERA)

                FIP = tds[12].text
                FIP = FIP.strip()
                playerData.append(FIP)

                leftOnBase = tds[13].text
                leftOnBase = leftOnBase.strip()
                playerData.append(leftOnBase)

                fbPercentage = tds[14].text
                fbPercentage = fbPercentage.strip()
                playerData.append(fbPercentage)

                hrFB = tds[15].text
                hrFB = hrFB.strip()
                playerData.append(hrFB)

                rotogrindersPitcherLSplitsData.append(playerData)

                pitchersLeftSplitsEntry = PitcherLeftSplits(parent=RotogrindersPitcherLSplitsEntry, name=playerName,
                                                            team=team, opponent=opponent,
                                                            avg=average, babip=babip, ip=inningsPitched, woba=wOBA,
                                                            knine=k9, bbPercentage=bbPercentage, whip=WHIP, era=ERA, fip=FIP,
                                                            lob=leftOnBase, fb=fbPercentage, hrfb=hrFB, ops=OPS)
                pitchersLeftSplitsEntry.save()

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotogrindersPitcherSplitsHeaders:
                html += '<th>'
                html += header
                html += '</th>'

            for player in rotogrindersPitcherLSplitsData:
                html += '<tr>'
                for data in player:
                    html += '<td>'
                    html += data
                    html += '</td>'
                html += '</tr>'

            html += '</table>'

            return HttpResponse(html)

        else:
            pitcherSplitsLeftData = PitcherLeftSplits.objects.filter(parent=request.data["id"])
            serializer = PitcherLeftSplitsSerializer(pitcherSplitsLeftData, many=True)
            pitcherLeftSplitsSerializedData = serializer.data

            rotogrindersPitcherSplitsHeaders = ["Name", "Team", "Opponent", "IP", "AVG", "wOBA", "OPS", "K/9", "BABIP",
                                                "BB%",
                                                "WHIP", "ERA", "FIP", "LOB%", "FB%", "HR/FB"]

            html = '<table class="table table-hover table-bordered table-striped">'

            for header in rotogrindersPitcherSplitsHeaders:
                html += '<th>'
                html += header
                html += '</th>'

            for player in pitcherLeftSplitsSerializedData:
                html += '<tr>'
                for i, (key, value) in enumerate(player.iteritems()):
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
def baseballRotogrindersLeftHandedBatterSplits(request):
    if request.method == 'POST':
        url = "https://rotogrinders.com/pages/mlb-player-statistics-catchers-vs-left-264413"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        batterSplitsHeader = ["Player", "Team", "GP", "AB", "H", "1B", "2B", "3B", "HR", "R", "RBI", "BB", "SO", "SB", "SF",
                              "GIDP", "AVG", "OBP", "SLG", "OBP"]

        batterLeftSplitsData = []

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterLeftSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-1st-base-vs-left-264414"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterLeftSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-2nd-base-vs-left-264416"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterLeftSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-3rd-base-vs-left-264417"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterLeftSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-shortstop-vs-left-264418"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterLeftSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-outfielders-vs-left-264419"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterLeftSplitsData.append(playerData)

        html = '<table class="table table-hover table-bordered table-striped">'

        for header in batterSplitsHeader:
            html += '<th>'
            html += header
            html += '</th>'

        for player in batterLeftSplitsData:
            html += '<tr>'
            for data in player:
                html += '<td>'
                html += data
                html += '</td>'
            html += '</tr>'

        html += '</table>'

        return HttpResponse(html)

@api_view(['POST', 'GET'])
def baseballRotogrindersRightHandedBatterSplits(request):
    if request.method == 'POST':
        url = "https://rotogrinders.com/pages/mlb-player-statistics-catchers-vs-right-264420"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        batterSplitsHeader = ["Player", "Team", "GP", "AB", "H", "1B", "2B", "3B", "HR", "R", "RBI", "BB", "SO", "SB", "SF",
                              "GIDP", "AVG", "OBP", "SLG", "OBP"]

        batterRightSplitsData = []

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterRightSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-1st-base-vs-right-264421"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterRightSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-2nd-base-vs-right-264422"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterRightSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-3rd-base-vs-right-264423"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterRightSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-shortstop-vs-right-264424"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterRightSplitsData.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-player-statistics-outfielders-vs-right-264425"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            team = tds[1].span
            team = team.text
            team = team.strip()
            playerData.append(team)

            gp = tds[2].text
            gp = gp.strip()
            playerData.append(gp)

            ab = tds[3].text
            ab = ab.strip()
            playerData.append(ab)

            hits = tds[4].text
            hits = hits.strip()
            playerData.append(hits)

            singles = tds[5].text
            singles = singles.strip()
            playerData.append(singles)

            doubles = tds[6].text
            doubles = doubles.strip()
            playerData.append(doubles)

            triples = tds[7].text
            triples = triples.strip()
            playerData.append(triples)

            hr = tds[8].text
            hr = hr.strip()
            playerData.append(hr)

            runs = tds[9].text
            runs = runs.strip()
            playerData.append(runs)

            rbi = tds[10].text
            rbi = rbi.strip()
            playerData.append(rbi)

            walks = tds[11].text
            walks = walks.strip()
            playerData.append(walks)

            strikouts = tds[12].text
            strikouts = strikouts.strip()
            playerData.append(strikouts)

            sb = tds[13].text
            sb = sb.strip()
            playerData.append(sb)

            sf = tds[14].text
            sf = sf.strip()
            playerData.append(sf)

            gidp = tds[15].text
            gidp = gidp.strip()
            playerData.append(gidp)

            avg = tds[16].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[17].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[18].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[19].text
            ops = ops.strip()
            playerData.append(ops)

            batterRightSplitsData.append(playerData)

        html = '<table class="table table-hover table-bordered table-striped">'

        for header in batterSplitsHeader:
            html += '<th>'
            html += header
            html += '</th>'

        for player in batterRightSplitsData:
            html += '<tr>'
            for data in player:
                html += '<td>'
                html += data
                html += '</td>'
            html += '</tr>'

        html += '</table>'

        return HttpResponse(html)

@api_view(['POST', 'GET'])
def baseballRotogrindersLeftHandedAdvancedBatterSplits(request):
    if request.method == 'POST':
        url = "https://rotogrinders.com/pages/mlb-advanced-stats-catcher-vs-left-264456"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        batterAdvancedSplitsHeader = ["Player", "PA", "AVG", "OBP", "SLG", "OPS", "K%", "BB/K", "ISO", "SPD", "BABIP", "wRC",
                                      "wRC", "wOBA"]

        batterLeftAdvancedSplitsHeader = []

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterLeftAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-1b-vs-left-264457"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterLeftAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-2b-vs-left-264458"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterLeftAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-3b-vs-left-264459"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterLeftAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-ss-vs-left-264460"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterLeftAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-of-vs-left-264461"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        lSplitsTable = soup.find_all('tbody')[0]

        for tr in lSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterLeftAdvancedSplitsHeader.append(playerData)

        html = '<table class="table table-hover table-bordered table-striped">'

        for header in batterAdvancedSplitsHeader:
            html += '<th>'
            html += header
            html += '</th>'

        for player in batterLeftAdvancedSplitsHeader:
            html += '<tr>'
            for data in player:
                html += '<td>'
                html += data
                html += '</td>'
            html += '</tr>'

        html += '</table>'

        return HttpResponse(html)

@api_view(['POST', 'GET'])
def baseballRotogrindersRightHandedAdvancedBatterSplits(request):
    if request.method == 'POST':
        url = "https://rotogrinders.com/pages/mlb-advanced-stats-catcher-vs-right-264462"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        batterAdvancedSplitsHeader = ["Player", "PA", "AVG", "OBP", "SLG", "OPS", "K%", "BB/K", "ISO", "SPD", "BABIP", "wRC",
                                      "wRC", "wOBA"]

        batterRightAdvancedSplitsHeader = []

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr')[:-1]:
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterRightAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-1b-vs-right-264463"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterRightAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-2b-vs-right-264464"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterRightAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-3b-vs-right-264465"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterRightAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-ss-vs-right-264466"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterRightAdvancedSplitsHeader.append(playerData)

        url = "https://rotogrinders.com/pages/mlb-advanced-stats-of-vs-right-264467"

        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")

        rSplitsTable = soup.find_all('tbody')[0]

        for tr in rSplitsTable.find_all('tr'):
            tds = tr.find_all('td')

            playerData = []

            playerName = tds[0].a
            if playerName is None:
                playerName = tds[0]
            playerName = playerName.text
            playerName = playerName.strip()
            playerData.append(playerName)

            pa = tds[1]
            pa = pa.text
            pa = pa.strip()
            playerData.append(pa)

            avg = tds[2].text
            avg = avg.strip()
            playerData.append(avg)

            obp = tds[3].text
            obp = obp.strip()
            playerData.append(obp)

            slg = tds[4].text
            slg = slg.strip()
            playerData.append(slg)

            ops = tds[5].text
            ops = ops.strip()
            playerData.append(ops)

            kPercentage = tds[6].text
            kPercentage = kPercentage.strip()
            playerData.append(kPercentage)

            BBPerK = tds[7].text
            BBPerK = BBPerK.strip()
            playerData.append(BBPerK)

            ISO = tds[8].text
            ISO = ISO.strip()
            playerData.append(ISO)

            SPD = tds[9].text
            SPD = SPD.strip()
            playerData.append(SPD)

            BABIP = tds[10].text
            BABIP = BABIP.strip()
            playerData.append(BABIP)

            wRC = tds[11].text
            wRC = wRC.strip()
            playerData.append(wRC)

            wRCPlus = tds[12].text
            wRCPlus = wRCPlus.strip()
            playerData.append(wRCPlus)

            wOBA = tds[13].text
            wOBA = wOBA.strip()
            playerData.append(wOBA)

            batterRightAdvancedSplitsHeader.append(playerData)

        html = '<table class="table table-hover table-bordered table-striped">'

        for header in batterAdvancedSplitsHeader:
            html += '<th>'
            html += header
            html += '</th>'

        for player in batterRightAdvancedSplitsHeader:
            html += '<tr>'
            for data in player:
                html += '<td>'
                html += data
                html += '</td>'
            html += '</tr>'

        html += '</table>'

        return HttpResponse(html)