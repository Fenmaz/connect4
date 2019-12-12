import numpy as np
#import pygame #brew install python3 && cp /usr/local/bin/python3 /usr/local/bin/python
import sys
import math
import random
import time

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board,col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board,piece):
    # check for all the horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check for all vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
'''
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2),r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2),RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
'''


def board_full(board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 0:
                return False
    return True

board = create_board()
game_over = False
turn = 0

#pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width,height)
RADIUS = int(SQUARESIZE/2 - 5)

#screen = pygame.display.set_mode(size)
#draw_board(board)
#pygame.display.update()


f = open("board_config.txt","a")

for cnt in range(10000):
    random.seed(time.clock())
    board = create_board()
    game_over = False
    turn = 0
    while not game_over:
        if board_full(board):
            print("DRAW!!!")
            game_over = True
            break
        if turn == 0:
            #posx = event.pos[0]
            #col = int(math.floor(posx/SQUARESIZE))
            col = random.randint(0,6)
            while not is_valid_location(board,col):
                col = random.randint(0,6)
            if is_valid_location(board,col):
                row = get_next_open_row(board,col)
                drop_piece(board,row,col,1)
                if winning_move(board,1):
                    print("Player 1 wins!")
                    game_over = True
                    break
        # Ask for player 2 input
        else:
            #posx = event.pos[0]
            #col = int(math.floor(posx/SQUARESIZE))
            col = random.randint(0,6)
            while not is_valid_location(board,col):
                col = random.randint(0,6)
            if is_valid_location(board,col):
                row = get_next_open_row(board,col)
                drop_piece(board,row,col,2)
                if winning_move(board,2):
                    print("Player 2 wins!")
                    game_over = True
                    break
        print_board(board)
        str = np.array2string(board.flatten()) + "\n\n"
        f.write(str)
        turn += 1
        turn = turn % 2
