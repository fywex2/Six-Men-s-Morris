import numpy as np
import random as rnd

"""
creating the board itself when empty by 7x7 numpy array
(0 is the places where pieces could be placed, -1 places where pieces can't be placed,
1 will be the white pieces that will be starting first, that can only be placed on places with the value of 0,
2 will be the black pieces that will be starting second, that can only be placed on places with the value of 0)
"""
class Game_NineMensMorris:
    def __init__(self):
        self.board = np.array([
            [0, -1, -1, 0, -1, -1, 0],
            [-1, 0, -1, 0, -1, 0, -1],
            [-1, -1, 0, 0, 0, -1, -1],
            [0,  0,  0, -1, 0,  0, 0],
            [-1, -1, 0, 0, 0, -1, -1],
            [-1, 0, -1, 0, -1, 0, -1],
            [0, -1, -1, 0, -1, -1, 0]
            ], dtype=np.int8)
        self.agent_pieces = 9  # the amount of total pieces of the agent
        self.opp_pieces = 9  # the amount of total pieces of the opponent
        self.agent_pieces_not_placed = 9  # the amount of pieces that wasn't place on the board of the agent
        self.opp_pieces_not_placed = 9  # the amount of pieces that wasn't place on the board of the opponent
        self.white_mills = 0  # white mills on the board
        self.black_mills = 0  # black mills on the board

    # returns a list of where pieces could be placed
    def legal_places_before(self):
        tupple_list = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 0:
                    tupple_list.append((i, j))
        return tupple_list

    # returns a list of where pieces could be moved to after all the pieces of the player where put on the board
    def legal_places_after(self, player):
        moves = []

        for i in range(7):
            for j in range(7):
                if self.board[i, j] == player:
                    adjacent_positions = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

                    for adj_i, adj_j in adjacent_positions:
                        if (0 <= adj_i < 7) and (0 <= adj_j < 7) and self.board[adj_i, adj_j] == 0:
                            moves.append(((i, j), (adj_i, adj_j)))

        return moves

    # returns a list of where pieces could be moved when there are 3 pieces left on the board (flying stage)
    def flying_stage_moves(self, player):
        moves = []

        for i in range(7):
            for j in range(7):
                if self.board[i][j] == player:
                    for x in range(7):
                        for y in range(7):
                            if self.board[x][y] == 0 and (i == x or j == y or abs(i - x) == abs(j - y)):
                                moves.append(((i, j), (x, y)))

        return moves

    # returns a list of where the white pieces are on the board
    def white_places(self):
        white_tuple = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 1:
                    white_tuple.append((i,j))
        return white_tuple

    # returns a list of where the black pieces are on the board
    def black_places(self):
        black_tuple = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 2:
                    black_tuple.append((i,j))
        return black_tuple

    # checks if there is a new line of 3 pieces of the selected player
    def check_new_mills(self, player):
        count = 0
        for i in range(7):
            if self.board[i, 0] == self.board[i, 1] == self.board[i, 2] == player:
                count += 1

            if self.board[0, i] == self.board[1, i] == self.board[2, i] == player:
                count += 1

        if player == 1:
            if count > self.white_mills:
                self.white_mills = count
                return True

        if player == 2:
            if count > self.black_mills:
                self.black_mills = count
                return True

        return False

    # return true if the parameter player have won and false else
    def check_winner(self):
        if self.opp_pieces_not_placed == 0 and not bool(self.legal_places_after(2)) or self.agent_pieces < 3:
            return 1
        if self.agent_pieces_not_placed == 0 and not bool(self.legal_places_after(1)) or self.opp_pieces < 3:
            return 2
        return 0

    # makes a random agent turn
    def agent_turn(self):
        if self.opp_pieces == 3 and self.opp_pieces_not_placed == 0:
            legal = self.flying_stage_moves(1)
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 1
            return
        if self.opp_pieces_not_placed == 0:
            legal = self.legal_places_after(1)
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 1
            return
        legal = self.legal_places_before()
        if len(legal) < 2:
            random_move = legal[0]
        else:
            random_move = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_move[0]][random_move[1]] = 1
        self.agent_pieces_not_placed -= 1
        if self.check_new_mills(1):
            self.remove_opp_piece()

    # remove random opponent's piece
    def remove_opp_piece(self):
        legal = self.white_places()
        if len(legal) < 2:
            random_remove = legal[0]
        else:
            random_remove = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_remove[0]][random_remove[1]] = 0
        self.opp_pieces -= 1

    # remove random agent's piece
    def remove_agent_piece(self):
        legal = self.black_places()
        if len(legal) < 2:
            random_remove = legal[0]
        else:
            random_remove = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_remove[0]][random_remove[1]] = 0
        self.agent_pieces -= 1

    # makes a random opponent turn
    def opp_turn(self):
        if self.opp_pieces == 3 and self.opp_pieces_not_placed == 0:
            legal = self.flying_stage_moves(2)
            random_move = legal[rnd.randint(0, len(legal)-1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 2
            return
        if self.opp_pieces_not_placed == 0:
            legal = self.legal_places_after(2)
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal)-1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 2
            return
        legal = self.legal_places_before()
        if len(legal) < 2:
            random_move = legal[0]
        else:
            random_move = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_move[0]][random_move[1]] = 2
        self.opp_pieces_not_placed -= 1
        if self.check_new_mills(2):
            self.remove_opp_piece()

class Games:
    def __init__(self):
        self.nmm = Game_NineMensMorris()  # object of the nine men's morris
        self.amount_games = 10  # amount of games to run
        self.white_wins = 0  # amount of wins for white
        self.black_wins = 0  # amount of wins for black

    # play a single game of nine men's morris
    def single_game(self):
        while self.nmm.check_winner() == 0:
            self.nmm.agent_turn()
            if self.nmm.check_winner() != 0:
                break
            self.nmm.opp_turn()
        return self.nmm.check_winner()

    # run a loop of the specified amount of games
    def multiply_games(self):
        for i in range(self.amount_games):
            game_result = self.single_game()
            if game_result == 1:
                self.white_wins += 1
            elif game_result == 2:
                self.black_wins += 1
            self.nmm = Game_NineMensMorris()


ninemensmorris = Games()
ninemensmorris.multiply_games()
print("Wins for white:", ninemensmorris.white_wins)
print("Wins for black:", ninemensmorris.black_wins)