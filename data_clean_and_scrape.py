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
test = refined[1:5001]
toExcel = []
cnt = 1
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
    #print(c)
    idx = c.find(":[")
    result = c[idx+2:-2]
    policy = result.split(',')
    toExcel.append(configs+policy)
    print("iteration %d" % cnt)
    cnt += 1

features = []
for i in range(1,43):
    features.append("pos_"+str(i))
for i in range(1,8):
    features.append("score_"+str(i))
df = pd.DataFrame(np.array(toExcel),columns=features)
df.to_csv('c4_generated.csv', index=False, encoding='utf-8')
