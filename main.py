from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
from easyAI import solve_with_iterative_deepening
import numpy as np

# black_square
even = [0, 2, 4, 6]
odd = [1, 3, 5, 7]

# init
even_row = [(i, j) for i in even for j in odd]
odd_row = [(i, j) for i in odd for j in even]

black_squares = even_row + odd_row


class Checker(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        # self.board = np.arange(8 * 8).reshape(8,8)
        self.blank_board = np.zeros((8, 8), dtype=object)
        self.board = self.blank_board.copy()
        self.black_pieces = [
            (0, 1), (0, 3), (0, 5), (0, 7),
            (1, 0), (1, 2), (1, 4), (1, 6)
        ]
        self.white_pieces = [
            (6, 1), (6, 3), (6, 5), (6, 7),
            (7, 0), (7, 2), (7, 4), (7, 6)
        ]
        for i, j in self.black_pieces:
            self.board[i, j] = "B"
        for i, j in self.white_pieces:
            self.board[i, j] = "W"

        self.white_territory = [(7, 0), (7, 2), (7, 4), (7, 6)]
        self.black_territory = [(0, 1), (0, 3), (0, 5), (0, 7)]

        self.players[0].pos = self.white_pieces
        self.players[1].pos = self.black_pieces

        self.current_player = 1  # player 1 starts.

    def possible_moves_on_white_turn(self):

        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p, l) in zip(self.players, ["W", "B"]):
            for x, y in p.pos:
                board[x, y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player - 1].pos:
            old_piece_pos = v

            step_pos = [(v[0] - 1, v[1] - 1), (v[0] - 1, v[1] + 1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B", "W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y, x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <= 7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos, j))
                    else:
                        old_new_piece_pos.append((old_piece_pos, n))

        # board position after  move
        for i, j in old_new_piece_pos:
            print(f"i = {i}")
            b = board.copy()
            b[i[0], i[1]] = 0  # old position
            b[j[0], j[1]] = "W"  # new position
            # print(b)
            table_pos.append(b)
            assert len(np.where(b != 0)[
                           0]) == 16, f"In possible_moves_on_white_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos

    def possible_moves_on_black_turn(self):
        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p, l) in zip(self.players, ["W", "B"]):
            for x, y in p.pos:
                board[x, y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player - 1].pos:
            old_piece_pos = v

            step_pos = [(v[0] + 1, v[1] - 1), (v[0] + 1, v[1] + 1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B", "W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y, x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <= 7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos, j))
                    else:
                        old_new_piece_pos.append((old_piece_pos, n))

        # board position after  move

        for i, j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = 0
            b[j[0], j[1]] = "B"
            table_pos.append(b)
            assert len(np.where(b != 0)[
                           0]) == 16, f"In possible_moves_on_black_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos

    def possible_moves(self):
        """
        """
        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()

    def get_piece_pos_from_table(self, table_pos):
        if self.current_player - 1 == 0:
            x = np.where(table_pos == "W")
        elif self.current_player - 1 == 1:
            x = np.where(table_pos == "B")
        else:
            raise ValueError("There can be at most 2 players.")

        assert len(np.where(table_pos != 0)[
                       0]) == 16, f"In get_piece_pos_from_table(), there are {len(np.where(table_pos != 0)[0])} pieces on the board  \n {table_pos}"
        return [(i, j) for i, j in zip(x[0], x[1])]






#************************ 4 of the functions implementations Explaination #**************************
    # I had implemented these 4 functions below, let me explain this very quickly.
    # I had chosen to implement them for the functions that they have connections to these 4 functions
    # make_move(), lose(), scoring() and is_over()
    # they are easily to be coded and very simply.
    # one function that I need to do is that the make_over(), this function allows us to
    # make the black_pieces and white_pieces on the board which the function is already made.
    # I just need to be called the function possible_moves() because it calls this function to start the checker
    # game. in this make_move() function, I did the first function call and Gamalie did the next function which
    # is self.players[self.current_player - 1].pos = self.get_piece_pos_from_table(pos) and we add one more thing
    # is to put the piece position from the table board. I did the lose(), is_over(), and scoring(). The
    # lose() function that I already looked over at the previous function that it has to do with the matrix from the
    # board. ex. is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
    # from self.players[self.current_player] and I return ture and false statements when they are reach to
    # the end of their opposite board lines. is_over() calls the function lose(). It is either continues to
    # make the possible next move or calls the function lose(), so I used the return value to indicates that.
    # scoring() is a function that gives points to the winner. maximum 10 points for the winner and 0 point for
    # the loser. In the main(), that I called the game.lose() and game.scoring() to call the def functions in the
    # file. Then they can print out the results.

    def make_move(self, pos):
        # I added the make_move *****************************
        #self.possible_moves()

        self.players[self.current_player - 1].pos = self.get_piece_pos_from_table(pos)
        self.board=pos
    def lose(self):

        for i in self.players[0].pos:
            if i in self.black_territory:
                self.won="White"
                return True

        for j in self.players[1].pos:
            if j in self.white_territory:
                self.won="Black"
                return True

        return False

    def is_over(self):

      return (self.possible_moves() == []) or self.lose()

    def show(self):
        """
        show 8*8 checker board.
        """

        # board position before move
        board = self.blank_board.copy()
        print(f"player 1 positions = {self.players[0].pos}")
        print(f"player 2 positions = {self.players[1].pos}")
        for (p, l) in zip(self.players, ['W', 'B']):
            for x, y in p.pos:
                board[x, y] = l
        print('\n')
        print(board)

    def scoring(self):
         return 0 if self.lose() else 10 #maximum 10 points else return 0

if __name__ == "__main__":
    ai = Negamax(1)  # The AI will think 13 moves in advance
    game = Checker([AI_Player(ai), AI_Player(ai)])
    history = game.play()
    if game.is_over():
     print("player %d wins"%(game.current_player))
    else:
        print("We have a draw")
    n=game.scoring()
    print("player %d"%(game.current_player)," score is ",(game.scoring()))
