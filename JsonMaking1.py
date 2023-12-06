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
        self.win_points_agent = 1  # points for the win of agent
        # self.tie_points = 0.5  # points for a tie
        self.loss_points_agent = 0  # points for a loss of agent
        self.states = []  # collecting states from a single game
        self.state_scores = []  # collecting scores for each state in the game
        self.gama = 0.9  # amount to multiply the state every new board

    # returns a list of where pieces could be placed
    def legal_places_before(self, player):
        moves_list = []
        if self.agent_pieces + self.opp_pieces < 18:
            for i in range(7):
                for j in range(7):
                    if self.board[i][j] == 0 and \
                       ((i == 0 or i == 3 or i == 6) and (j == 0 or j == 3 or j == 6) or \
                       (i == 1 or i == 5) and (j == 1 or j == 5) or \
                       (i == 2 or i == 4) and (j == 2 or j == 4)):
                        moves_list.append((i, j))
        return moves_list


    # returns a list of where pieces could be moved to after all the pieces of the player where put on the board
    def legal_places_after(self, player):
        moves_list = []
        # Check how many pieces the player has
        if player == 1:
            num_pieces = self.agent_pieces
        else:
            num_pieces = self.opp_pieces
        # Loop through the board positions
        for i in range(7):
            for j in range(7):
                # Check if the position has the player's piece
                if self.board[i, j] == player:
                    # If the player has three pieces, they can fly to any empty point
                    if num_pieces == 3:
                        for k in range(7):
                            for l in range(7):
                                if self.board[k, l] == 0 and \
                                   ((k == 0 or k == 3 or k == 6) and (l == 0 or l == 3 or l == 6) or \
                                   (k == 1 or k == 5) and (l == 1 or l == 5) or \
                                   (k == 2 or k == 4) and (l == 2 or l == 4)):
                                    moves_list.append(((i, j), (k, l)))
                    # Otherwise, they can only move to adjacent points
                    else:
                        adjacent_positions = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                        for adj_i, adj_j in adjacent_positions:
                            if (0 <= adj_i < 7) and (0 <= adj_j < 7) and self.board[adj_i, adj_j] == 0 and \
                               ((adj_i == 0 or adj_i == 3 or adj_i == 6) and (adj_j == 0 or adj_j == 3 or adj_j == 6) or \
                               (adj_i == 1 or adj_i == 5) and (adj_j == 1 or adj_j == 5) or \
                               (adj_i == 2 or adj_i == 4) and (adj_j == 2 or adj_j == 4)):
                                moves_list.append(((i, j), (adj_i, adj_j)))
        return moves_list



    # returns a list of where pieces could be moved when there are 3 pieces left on the board (flying stage)
    def flying_stage_moves(self, player):
        moves_list = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == player:
                    for x in range(7):
                        for y in range(7):
                            if self.board[x][y] == 0 and (i == x or j == y or abs(i - x) == abs(j - y)):
                                moves_list.append(((i, j), (x, y)))
        return moves_list

    # returns a list of where the white pieces are on the board
    def white_places(self):
        white_locations = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 1:
                    white_locations.append((i,j))
        return white_locations

    # returns a list of where the black pieces are on the board
    def black_places(self):
        black_locations = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 2:
                    black_locations.append((i,j))
        return black_locations

    # checks if there is a new line of 3 pieces of the selected player
    def check_new_mills(self, player):
        count = 0
        for i in range(7):
            if self.board[i, 0] == self.board[i, 1] == self.board[i, 2] == player:
                count += 1
            if self.board[0, i] == self.board[1, i] == self.board[2, i] == player:
                count += 1
        if player == 1:
            self.white_mills = count
            if count > self.white_mills:
                return True
        if player == 2:
            self.black_mills = count
            if count > self.black_mills:
                return True
        return False

    # return true if the parameter player have won and false else
    def check_winner(self):
        if (self.opp_pieces_not_placed == 0 and not bool(self.legal_places_after(2))) or self.agent_pieces < 3:
            return 1
        if (self.agent_pieces_not_placed == 0 and not bool(self.legal_places_after(1))) or self.opp_pieces < 3:
            return 2
        return 0

    # makes a random agent turn
    def agent_turn(self):
        if self.opp_pieces == 3 and self.opp_pieces_not_placed == 0:
            legal = self.flying_stage_moves(1)
            if len(legal) == 0:
                return
            if len(legal) < 1:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 1
            return
        if self.opp_pieces_not_placed == 0:
            legal = self.legal_places_after(1)
            if len(legal) == 0:
                return
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 1
            return
        legal = self.legal_places_before(1)
        if len(legal) == 0:
            return
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
        if len(legal) == 0:
            return
        if len(legal) < 2:
            random_move = legal[0]
        else:
            random_remove = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_remove[0]][random_remove[1]] = 0
        self.opp_pieces -= 1

    # remove random agent's piece
    def remove_agent_piece(self):
        legal = self.black_places()
        if len(legal) == 0:
            return
        if len(legal) < 2:
            random_move = legal[0]
        else:
            random_remove = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_remove[0]][random_remove[1]] = 0
        self.agent_pieces -= 1

    # makes a random opponent turn
    def opp_turn(self):
        if self.opp_pieces == 3 and self.opp_pieces_not_placed == 0:
            legal = self.flying_stage_moves(2)
            if len(legal) == 0:
                return
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 2
            return
        if self.opp_pieces_not_placed == 0:
            legal = self.legal_places_after(2)
            if len(legal) == 0:
                return
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 2
            return
        legal = self.legal_places_before(2)
        if len(legal) == 0:
            return
        if len(legal) < 2:
            random_move = legal[0]
        else:
            random_move = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_move[0]][random_move[1]] = 2
        self.opp_pieces_not_placed -= 1
        if self.check_new_mills(2):
            self.remove_agent_piece()
            

class Games:
    def __init__(self):
        self.nmm = Game_NineMensMorris()  # object of the nine men's morris
        self.amount_games = 1  # amount of games to run
        self.white_wins = 0  # amount of wins for white
        self.black_wins = 0  # amount of wins for black

    # play a single game of nine men's morris
    def single_game(self):
        while self.nmm.check_winner() == 0:
            self.nmm.agent_turn()
            # print(self.nmm.board)
            if self.nmm.check_winner() != 0:
                break
            self.nmm.opp_turn()
            # print(self.nmm.board)
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


run_games = Games()
run_games.multiply_games()
print("Wins for white:", run_games.white_wins)
print("Wins for black:", run_games.black_wins)