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

ExpW = [0]*10
hadGame = [[False]*10 for _ in range(10)]

for i in range(len(History)):
    team1, team2, isTeam1W = History[i]
    hadGame[team1][team2] = True
    hadGame[team2][team1] = True
    
    if isTeam1W:
        ExpW[team1] += 1
    else:
        ExpW[team2] += 1

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

for team1 in range(10):
    for team2 in range(team1):
        if team1 != team2 and not hadGame[team1][team2]:
            ExpW[team1] += W_e(Elo[team1], Elo[team2])
            ExpW[team2] += 1 - W_e(Elo[team1], Elo[team2])

Enum.sort(key = lambda x:-ExpW[Team[x]])
ExpW.sort(key = lambda x:-x)

for i in range(10):
    print(i+1, Enum[i], ExpW[i]*100//1/100)