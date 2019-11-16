'''
Aim is to create a solver that outputs how many steps are left
to end up with a win/lose/draw for the current player.

I am assuming that it's player 1's turn given the current
configuration of the board.

I referred to an example of the Negamax solver: http://blog.gamesolver.org/solving-connect-four/03-minmax/

I first read the data from connect-4.data and then organize them into grid form.

Similar to what the author in the above link did, I place 1 for player 1, 2 for player 2 and 0 for blank cells

Then using the scoring method described in the above link, I try to run the negamax algorithm.

'''
import data_util

'''================== I/O Methods ====================='''
'''
If the cell in the board is blank, assign 0
If the cell in the board is taken by player 1, assign 1
If the cell in the board is taken by player 2, assign 2
'''
def assign(c):
    if c == "b":
        return 0
    elif c == "x":
        return 1
    elif c == "o":
        return 2
'''
Convert the given data string to a 6x7 board
Return the board and the win/loss/draw tag for the first player.
'''
def toBoard(pos):
    # declare an nxm board
    n = 6
    m = 7
    board = [[0]*m for i in range(n)]
    pos = pos.split(',')
    i = 0
    col = 0
    while i < len(pos)-1:
        for j in range(6):
            row = 5-j
            board[row][col] = assign(pos[i+j])
        i += 6
        col += 1
    return([board,pos[len(pos)-1]])

'''
Extract data line by line from the given connect-4.data
We return each of the 6x7 board configuration as well as
the win/loss/draw tag for the first player for each configuration
'''
def Positions(filepath):
    data = []
    with open(filepath) as fp:
        for cnt,line in enumerate(fp):
            line = line[:-1]
            data.append(line)
    fp.close()
    ret = [] # array containing tuple: (6x7 board, win/loss/draw tag)
    for pos in data:
        ret.append(toBoard(pos))
    return(ret)

'''================== Storing board information and solving ====================='''

'''
The Board class contains information about the given configuration of the board,
as well as whether the current player will win/lose or end up in a draw if he/she makes a
move on the given board. Also contains information about the dimension of the board.
'''
class Board:
    def __init__(self,board,status,moves=0,row=6,col=7):
        self.board = board
        self.status = status
        self.moves = moves
        self.row = row
        self.col = col
        # we fill up the height information for each column
        self.height = [0]*col
        for i in range(self.col):
            for j in range(self.row):
                if self.board[self.row-j-1][i] != 0:
                    self.height[i] += 1

    def Moves(self):
        return(self.moves)

    def canPlace(self,pos): #pos = which column number
        return(self.height[pos] < self.row)

    def Place(self,pos):
        if self.height[pos] < 6:
            self.board[self.height[pos]][pos] = 1+self.moves%2
            self.height[pos] += 1
            self.moves += 1

    '''
    Indicates if the player will win by placing
    on the given column (pos). We can optimize using method used by Trung (bit configurations stored in hash map)
    The current implementation is a bit messy
    '''
    def isWinningMove(self,pos):
        current_player = 1+self.moves%2
        # vertical check
        if self.height[pos] >= 3 and self.board[self.height[pos]-1][pos] == current_player and self.board[self.height[pos]-2][pos] == current_player and self.board[self.height[pos]-1][pos] == current_player:
            return True
        # horizontal check in left direction
        x = self.height[pos]
        y = pos-1
        cnt = 0
        while y >= 0 and y < self.col and self.board[x][y] == current_player:
            y -= 1
            cnt += 1
        if cnt == 3:
            return True
        # horizontal check in right direction
        cnt = 0
        y = pos+1
        while y >= 0 and y < self.col and self.board[x][y] == current_player:
            y += 1
            cnt += 1
        if cnt == 3:
            return True
        # diagonal NW direction
        cnt = 0
        x = self.height[pos]-1
        y = pos-1
        while x >= 0 and x < self.row and y >= 0 and y < self.col and self.board[x][y] == current_player:
            x -= 1
            y -= 1
            cnt += 1
        if cnt == 3:
            return True
        # diagonal NE direction
        cnt = 0
        x = self.height[pos]-1
        y = pos+1
        while x >= 0 and x < self.row and y >= 0 and y < self.col and self.board[x][y] == current_player:
            x -= 1
            y += 1
            cnt += 1
        if cnt == 3:
            return True
        # diagonal SW direction
        cnt = 0
        x = self.height[pos]+1
        y = pos-1
        while x >= 0 and x < self.row and y >= 0 and y < self.col and self.board[x][y] == current_player:
            x += 1
            y -= 1
            cnt += 1
        if cnt == 3:
            return True
        # diagonal SE direction
        cnt = 0
        x = self.height[pos]+1
        y = pos+1
        while x >= 0 and x < self.row and y >= 0 and y < self.col and self.board[x][y] == current_player:
            x += 1
            y += 1
            cnt += 1
        if cnt == 3:
            return True
        # if the checks all fail
        return False
'''
Using scoring metric defined in
http://blog.gamesolver.org/solving-connect-four/02-test-protocol/
Once we obtain the score, we can also use this information to figure out the number of steps until the current player wins/loses/draws.
This implementation does not work because it exceeds maximum recursion depth.
Also it is extremely slow.
'''
def Negamax(board): # board is an instance of Board
    if board.Moves() == board.row * board.col:
        return 0
    for pos in range(board.col):
        if board.canPlace(pos) == True and board.isWinningMove(pos) == True:
            return (board.row * board.col + 1 - board.Moves())/2
    best = -board.row*board.col
    for pos in range(board.col):
        if board.canPlace(pos) == True:
            Board2 = Board(board.board,board.status)
            Board2.Place(pos)
            score = -Negamax(Board2)
            if score > best:
                best = score
    return best

''' printing out grid for debugging purposes '''
def printGrid(a):
    for i in range(6):
        for j in range(7):
            print(a[i][j],end='')
        print()

'''================== Main Function ====================='''
if __name__ == "__main__":
    data_util.download()  # download data if it is not already available
    filepath = 'data/connect-4.data'
    ret = Positions(filepath)
    test = ret[0]
    b = Board(test[0],test[1])
    score = Negamax(b)
    print(score)
