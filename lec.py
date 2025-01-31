from pprint import pprint
import csv

Team = {"G2":0, "FNC":1, "MKOI":2, "BDS":3, "SK":4, "GX":5, "TH":6, "VIT":7, "KC":8, "RGE":9}
Enum = ["G2", "FNC", "MKOI", "BDS", "SK", "GX", "TH", "VIT", "KC", "RGE"]
Elo = [1606, 1498, 1390, 1480, 1349, 1312, 1292, 1305, 1340, 1223]
K = 33
x = 400

History = []
with open('history.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row[0] == "TEAM1": continue
        team1, team2, isTeam1W = Team[row[0]], Team[row[1]], row[2] == "1"
        History.append((team1, team2, isTeam1W))

Standing = [0]*10
hadGame = [[False]*10 for _ in range(10)]

for i in range(len(History)):
    team1, team2, isTeam1W = History[i]
    hadGame[team1][team2] = True
    hadGame[team2][team1] = True
    
    if isTeam1W:
        Standing[team1] += 1
    else:
        Standing[team2] += 1

def W_e(elo1, elo2):
    return 1/(10**((elo2-elo1)/400)+1)

def updateElo(Elo, team1, team2, isTeam1W):
    diff = K * (isTeam1W - W_e(Elo[team1], Elo[team2]))
    if isTeam1W:
        Elo[team1] += diff
        Elo[team2] -= diff
    else:
        Elo[team1] -= diff
        Elo[team2] += diff

for i in range(len(History)):
    team1, team2, isTeam1W = History[i]
    updateElo(Elo, team1, team2, isTeam1W)

ExpW = Standing[:]
for team1 in range(10):
    for team2 in range(team1):
        if not hadGame[team1][team2]:
            ExpW[team1] += W_e(Elo[team1], Elo[team2])
            ExpW[team2] += 1 - W_e(Elo[team1], Elo[team2])

LeftGames = [] 
for team1 in range(10):
    for team2 in range(team1):
        if not hadGame[team1][team2]:
            LeftGames.append((team1, team2))

PORatio = [0]*10
for gameResult in range(2**len(LeftGames)):
    weight = 1
    PsStanding = Standing[:]
    for team1, team2 in LeftGames:
        isTeam1W = gameResult % 2
        gameResult //= 2
        
        if isTeam1W:
            PsStanding[team1] += 1
            weight *= W_e(Elo[team1], Elo[team2])
        else:
            PsStanding[team2] += 1
            weight *= 1 - W_e(Elo[team1], Elo[team2])
    PsEnum = Enum[:]
    PsEnum.sort(key = lambda x:-PsStanding[Team[x]])
    PsStanding.sort(key = lambda x:-x)
    if PsStanding[7] == PsStanding[8]:
        i = 0
        while i < 10 and PsStanding[i] != PsStanding[7]:
            PORatio[Team[PsEnum[i]]] += weight
            i += 1
        j = 0
        while i < 10 and PsStanding[i] == PsStanding[7]:
            i += 1
            j += 1
        i -= j
        for k in range(i, i+j):
            PORatio[Team[PsEnum[k]]] += weight*(8-i)/j
        
    else:
        for i in range(8):
            PORatio[Team[PsEnum[i]]] += weight

Enum.sort(key = lambda x:-PORatio[Team[x]])
ExpW.sort(key = lambda x:-x)
PORatio.sort(key = lambda x:-x)

for i in range(10):
    print(i+1, Enum[i], ExpW[i]*100//1/100, "{0}%".format(PORatio[i]*1000000//1/10000) if PORatio[i]*1000000//1/10000 != 99.9999 else "확정")