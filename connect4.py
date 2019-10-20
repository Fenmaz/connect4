def winning_sequences(n, k):
    assert(n >= k)
    basic_seqs = [2 ** k - 1]
    for i in range(n - k):
        basic_seqs.append(basic_seqs[-1] - 2 ** i + 2 ** (i + k))

    all_seqs = [2 ** k - 1]
    for i in range(2 ** k - 1, 2 ** n):
        for basic in basic_seqs:
            if i & basic == basic:
                all_seqs.append(i)
                break

    return frozenset(all_seqs)


class Connect4Board:
    """
    Represents a board of the Connect Four game.
    """
    def __init__(self):
        # Player turn: True - first, False - second
        self.turn = True

        # Keep track of where the next disc should fall to
        self.columns_total = [0] * 6

        # Encode all played discs with integers for checking win conditions
        self.columns = [[0] * 6, [0] * 6]
        self.rows = [[0] * 7, [0] * 7]
        # North-West diagonals, indexed by i+j
        self.nw_diag = [[0] * 12, [0] * 12]
        # North-East diagonals, indexed by i-j+6
        self.ne_diag = [[0] * 12, [0] * 12]

        # Generate all winning sequences for checking win conditions
        self.winning_sequences = winning_sequences(7, 4)

    def reset(self):
        """
        Reset the board to an empty board and start a new game.
        """
        self.turn = True
        self.columns_total = [0] * 6
        self.columns = [[0] * 6, [0] * 6]
        self.rows = [[0] * 7, [0] * 7]
        self.nw_diag = [[0] * 12, [0] * 12]
        self.ne_diag = [[0] * 12, [0] * 12]

    def play(self, column):
        """
        Play the next move on the board and switch to the opponent's turn.
        :param column: The column to drop the next disc in
        :return: True if the player who made this move won the game.
        """
        row = self.columns_total[column]
        self.columns_total[column] += 1

        self.columns[self.turn][column] += 2 ** row
        self.rows[self.turn][row] += 2 ** column
        self.nw_diag[self.turn][row + column] += 2 ** row
        self.ne_diag[self.turn][row - column + 6] += 2 ** row

        if self.columns[self.turn][column] in self.winning_sequences or \
           self.rows[self.turn][row] in self.winning_sequences or \
           self.nw_diag[self.turn][row + column] in self.winning_sequences or \
           self.ne_diag[self.turn][row - column + 6] in self.winning_sequences:

            self.turn = not self.turn
            return True

        self.turn = not self.turn
        return False


def ask_move(player, board_):
    move = int(input("Player {}'s turn.\n"
                     "Select a column to place a disc [1-7]: "
                     .format(player))) - 1
    win_ = board_.play(move)

    new_game_ = False
    continue__ = True
    if win_:
        print("Player {} won! Congratulations!".format(player))
        new_game_ = int(input("Start a new game? [0/1]: "))
        if not new_game_:
            print("Thanks for playing!")
            continue__ = False

    return continue__, new_game_


if __name__ == "__main__":
    board = Connect4Board()
    new_game = True
    continue_ = True
    while continue_:
        if new_game:
            print("Welcome to Connect4! Let's play!")
            board.reset()
            new_game = False

        continue_, new_game = ask_move("1", board)
        if continue_ and not new_game:
            continue_, new_game = ask_move("2", board)
