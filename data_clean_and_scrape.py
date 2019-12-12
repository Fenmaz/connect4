import csv
import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import copy

with open("board_config.txt") as fp:
   content = fp.readlines()
#0,1
#3,4
#6,7
# so basically spaced every 3 lines
set = set()
for i in range(0,len(content),3):
    combination = content[i]+content[i+1]
    set.add(combination)

l = []
for x in set:
    l.append(x)


refined = []

for s in l:
    cur = s
    cur = cur[1:-2]
    toList = cur.split(". ")
    idx = -1
    for i in range(len(toList)):
        if len(toList[i]) == 5:
            idx = i
            break
    if idx == -1:
        refined.append(toList)
        continue
    #print(toList[idx])
    #print(len(toList[idx]))
    temp = toList[idx][4]
    toList[idx] = toList[idx][0]
    toList.insert(idx+1,temp)
    toList[len(toList)-1] = toList[len(toList)-1][0]
    refined.append(toList)


def allZero(grid):
    for j in grid:
        if j != '0':
            return False
    return True

def deduceMoves(grid):
    temp = grid
    moves = []
    level = [0,0,0,0,0,0,0]
    turn = '1'
    cnt = 0
    while not allZero(temp):
        for i in range(0,len(temp)):
            if temp[i] == turn and (i <= 6 or level[i%7] >= 1):
                level[i%7] += 1
                moves.append(i%7+1)
                temp[i] = '0'
                break
        if turn == '1':
            turn = '2'
        elif turn == '2':
            turn = '1'
        cnt += 1
    return moves

# setup driver
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
test = refined[0:6000]
toExcel = []
#boardValue = [] # win/loss/draw status of the board (assuming perfect play)
#movesLeft = [] # number of moves left for the game to finish (assuming perfect play)
cnt = 1
'''
Red = player 1
Yellow = player 2
returns [boardValue,movesLeft]
'''
def gameStatus(s,query):
    if s == "Yellow won":
        return [2,0]
    elif s == "Red won":
        return [1,0]
    elif s == "Draw game":
        return [0,0]
    elif s == "Red can draw":
        return [0,42-len(query)]
    elif s == "Yellow can draw":
        return [0,42-len(query)]
    else: # either Red or Yellow wins with x number of moves left
        moves = [int(i) for i in s.split() if i.isdigit()]
        if s.find("Red") != -1 and s.find("win") != -1: # red found and wins
            return [1,moves[0]]
        elif s.find("Yellow") != -1 and s.find("win") != -1: # yellow found and wins
            return [2,moves[0]]
        elif s.find("Red") != -1 and s.find("loses") != -1: # red found and loses
            return [2,moves[0]]
        elif s.find("Yellow") != -1 and s.find("loses") != -1: # yellow found and loses
            return [1,moves[0]]

for configs in test:
    temp = copy.deepcopy(configs)
    output = deduceMoves(temp)
    query = ''.join(map(str,output))
    url = "https://connect4.gamesolver.org/solve?pos="+query
    scores = [0,0,0,0,0,0,0]
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    c = soup.getText()
    idx = c.find(":[")
    result = c[idx+2:-2]
    policy = result.split(',')
    # we now look up the board status and the number of moves to win
    url = "https://connect4.gamesolver.org/?pos="+query
    driver.get(url)
    time.sleep(2) # wait for a while after the website loads
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    c = soup.find("div",{"id":"solution_header"})
    ret = gameStatus(c.text,query)
    print("iteration %d" % cnt)
    print(configs)
    print(policy)
    print(ret)
    if type(configs) == type(policy) and type(configs) == type(ret) and type(policy) == type(ret):
        toExcel.append(configs+policy+ret)
    cnt += 1

features = []
for i in range(1,43):
    features.append("pos_"+str(i))
for i in range(1,8):
    features.append("score_"+str(i))
features.append("boardValue")
features.append("movesLeft")
df = pd.DataFrame(np.array(toExcel),columns=features)
df.to_csv('c4_generated.csv', index=False, encoding='utf-8')
