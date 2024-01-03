import numpy as np
import random as rnd
import time
import json
from collections import defaultdict

start_time = time.time()

"""
creating the board itself when empty by 5x5 numpy array
(0 is the places where pieces could be placed, 6 places where pieces can't be placed,
1 will be the white pieces that will be starting first, that can only be placed on places with the value of 0,
2 will be the black pieces that will be starting second, that can only be placed on places with the value of 0)
"""


class Game_NineMensMorris:
    def __init__(self):
        self.board = [
            [0, 9, 0, 9, 0],
            [9, 0, 0, 0, 9],
            [0, 0, 9, 0, 0],
            [9, 0, 0, 0, 9],
            [0, 9, 0, 9, 0]
        ]
        self.agent_pieces = 6  # the amount of total pieces of the agent
        self.opp_pieces = 6  # the amount of total pieces of the opponent
        self.agent_pieces_not_placed = 6  # the amount of pieces that wasn't place on the board of the agent
        self.opp_pieces_not_placed = 6  # the amount of pieces that wasn't place on the board of the opponent
        self.white_mills = 0  # white mills on the board
        self.black_mills = 0  # black mills on the board
        self.possible_mills = [
            # Horizontal mills on the first row
            [[0, 0], [0, 1], [0, 2]],
            [[0, 2], [1, 2], [2, 2]],
            [[2, 2], [2, 1], [2, 0]],
            [[2, 0], [1, 0], [0, 0]],

            # Horizontal mills on the second row
            [[0, 2], [0, 3], [0, 4]],
            [[0, 4], [1, 4], [2, 4]],
            [[2, 4], [2, 3], [2, 2]],
            [[2, 2], [1, 2], [0, 2]],

            # Horizontal mills on the third row
            [[1, 1], [1, 2], [1, 3]],
            [[1, 3], [2, 3], [3, 3]],
            [[3, 3], [3, 2], [3, 1]],
            [[3, 1], [2, 1], [1, 1]],

            # Vertical mills on the first column
            [[0, 1], [0, 3], [0, 4]],
            [[1, 2], [1, 3], [1, 4]],
            [[2, 1], [2, 3], [2, 4]],
            [[1, 0], [1, 2], [1, 4]]
        ]
        self.possible_adj = {
            (0, 0): [(0, 2), (2, 0)],
            (0, 2): [(0, 0), (0, 4), (1, 2)],
            (0, 4): [(2, 4), (0, 2)],
            (1, 1): [(1, 2), (2, 1)],
            (1, 2): [(1, 1), (1, 3), (0, 2)],
            (1, 3): [(1, 2), (2, 3)],
            (2, 0): [(0, 0), (4, 0), (2, 1)],
            (2, 1): [(2, 0), (1, 1), (3, 1)],
            (2, 3): [(2, 4), (1, 3), (3, 3)],
            (2, 4): [(0, 4), (4, 4), (2, 3)],
            (3, 1): [(2, 1), (3, 2)],
            (3, 2): [(4, 2), (3, 1), (3, 3)],
            (3, 3): [(3, 2), (2, 3)],
            (4, 0): [(2, 0), (4, 2)],
            (4, 2): [(3, 2), (4, 0), (4, 4)],
            (4, 4): [(4, 2), (2, 4)]
        }
        self.win_points_agent = 10  # points for the win of agent
        self.loss_points_agent = 0  # points for a loss of agent
        self.states = []  # collecting states from a single game
        self.state_scores = []  # collecting scores for each state in the game
        self.gama = 0.9  # amount to multiply the state every new board
        self.num_moves = 0

    def rank_board_state(self):
        rank = 10 * self.gama ** self.num_moves
        if self.check_winner() == 1:
            rank = self.win_points_agent
        if self.check_winner() == 2:
            rank = self.loss_points_agent

        rank = float(rank)

        flattened_board = [element for sublist in self.board for element in sublist]
        self.states.append(''.join(map(str, flattened_board)))
        self.state_scores.append(rank)

    # returns a list of where pieces could be placed
    def legal_places_before(self):
        moves_list = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0:
                    moves_list.append((i, j))
        return moves_list

    # returns a list of where pieces could be moved to after all the pieces of the player where put on the board
    def legal_places_after(self, player):
        moves_list = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == player:
                    adjacent_positions = self.possible_adj[i, j]
                    temp_moves = []

                    for position in adjacent_positions:
                        x, y = position
                        if self.board[x][y] == 0:
                            temp_moves.append(position)

                    if len(temp_moves) == 0:
                        continue

                    moves_list.append([(i, j), temp_moves])

        return moves_list

    # returns a list of where pieces could be moved when there are 3 pieces left on the board (flying stage)
    def flying_stage_moves(self, player):
        moves_list = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == player:
                    for x in range(5):
                        for y in range(5):
                            if self.board[x][y] == 0 and (i == x or j == y or abs(i - x) == abs(j - y)):
                                moves_list.append(((i, j), (x, y)))
        print("*")
        return moves_list

    # returns a list of where the white pieces are on the board
    def white_places(self):
        white_locations = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 1:
                    white_locations.append((i, j))
        return white_locations

    # returns a list of where the black pieces are on the board
    def black_places(self):
        black_locations = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 2:
                    black_locations.append((i, j))
        return black_locations

    # checks if there is a new line of 3 pieces of the selected player
    def check_new_mills(self, player):
        count = 0

        for mill in self.possible_mills:
            if self.board[mill[0][0]][mill[0][1]] == self.board[mill[1][0]][mill[1][1]] == self.board[mill[2][0]][mill[2][1]] == player:
                count += 1
        if player == 1:
            prev = self.white_mills
            if count > prev:
                self.white_mills = count
                return True
        if player == 2:
            prev = self.black_mills
            if count > prev:
                self.black_mills = count
                return True
        return False

    # return 1 if white won 2 if black won 0 if no one won
    def check_winner(self):
        if (self.opp_pieces_not_placed == 0 and self.opp_pieces > 3 and len(self.legal_places_after(2)) == 0) \
             or (self.opp_pieces == 3 and len(self.flying_stage_moves(2)) == 0) or self.opp_pieces < 3:
            return 1
        if (self.agent_pieces_not_placed == 0 and self.agent_pieces > 3 and len(self.legal_places_after(1)) == 0) \
             or (self.agent_pieces == 3 and len(self.flying_stage_moves(1)) == 0) or self.agent_pieces < 3:
            return 2
        if self.num_moves > 99:
            return -1
        return 0

    # makes a random agent turn
    def agent_turn(self):
        if self.agent_pieces == 3 and self.agent_pieces_not_placed == 0:
            legal = self.flying_stage_moves(1)
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[1][rnd.randint(0, 1)]] = 0
            self.board[random_move[1][0]][random_move[1][1]] = 1
        if self.agent_pieces_not_placed == 0:
            legal = self.legal_places_after(1)
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            if len(random_move[1]):
                temp_random = random_move[1][0]
            else:
                temp_random = random_move[1][rnd.randint(0, 1)]
            self.board[temp_random[0]][temp_random[1]] = 1
        if self.agent_pieces_not_placed > 0:
            legal = self.legal_places_before()
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0]][random_move[1]] = 1
            self.agent_pieces_not_placed -= 1
        self.rank_board_state()
        if self.check_new_mills(1):
            self.remove_opp_piece()
            self.rank_board_state()
            self.num_moves += 1
        self.num_moves += 1

    def remove_pieces_in_mills(self, player):

        pieces_to_remove = []
        if player == 1:
            for piece in self.white_places():
                for mill in self.possible_mills:
                    # Check if the black piece is in the current mill
                    if piece in mill:
                        # Check if all other pieces in the mill are also black
                        if all(other_piece in self.white_places() for other_piece in mill):
                            pieces_to_remove.append(piece)
                            break  # No need to check other mills, already part of one
            return [piece for piece in self.white_places() if piece not in pieces_to_remove]
        else:
            for piece in self.black_places():
                for mill in self.possible_mills:
                    # Check if the black piece is in the current mill
                    if piece in mill:
                        # Check if all other pieces in the mill are also black
                        if all(other_piece in self.black_places() for other_piece in mill):
                            pieces_to_remove.append(piece)
                            break  # No need to check other mills, already part of one
            return [piece for piece in self.black_places() if piece not in pieces_to_remove]

    # remove random opponent's piece
    def remove_opp_piece(self):
        legal = self.remove_pieces_in_mills(2)
        if len(legal) < 2:
            random_remove = legal[0]
        else:
            random_remove = legal[rnd.randint(0, len(legal) - 1)]
        self.board[random_remove[0]][random_remove[1]] = 0
        self.opp_pieces -= 1

    # remove random agent's piece
    def remove_agent_piece(self):
        legal = self.remove_pieces_in_mills(1)
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
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            self.board[random_move[1][rnd.randint(0, 1)]] = 2
        if self.opp_pieces_not_placed == 0:
            legal = self.legal_places_after(2)
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0][0]][random_move[0][1]] = 0
            if len(random_move[1]):
                temp_random = random_move[1][0]
            else:
                temp_random = random_move[1][rnd.randint(0, 1)]
            self.board[temp_random[0]][temp_random[1]] = 2
        if self.opp_pieces_not_placed > 0:
            legal = self.legal_places_before()
            if len(legal) < 2:
                random_move = legal[0]
            else:
                random_move = legal[rnd.randint(0, len(legal) - 1)]
            self.board[random_move[0]][random_move[1]] = 2
            self.opp_pieces_not_placed -= 1
        self.rank_board_state()
        if self.check_new_mills(2):
            self.remove_agent_piece()
            self.rank_board_state()
            self.num_moves += 1
        self.num_moves += 1


class Games:
    def __init__(self):
        self.nmm = Game_NineMensMorris()  # object of the nine men's morris
<<<<<<< Updated upstream
        self.amount_games = 1000  # amount of games to run
=======
        self.amount_games = 10  # amount of games to run
>>>>>>> Stashed changes
        self.white_wins = 0  # amount of wins for white
        self.black_wins = 0  # amount of wins for black

    # play a single game of nine men's morris
    def single_game(self):
        while self.nmm.check_winner() == 0:
            self.nmm.agent_turn()
            #print(self.nmm.board)
            if self.nmm.check_winner() != 0:
                break
            self.nmm.opp_turn()
            #print(self.nmm.board)
        #print(self.nmm.board)
        #print(self.nmm.num_moves)
        return self.nmm.check_winner()

    # run a loop of the specified amount of games
    def multiply_games(self):
        aggregated_dict = defaultdict(lambda: {'total_rank': 0, 'count': 0})

        with open('GameData.json', 'r') as file:
            existing_data = json.load(file)

        for i in range(self.amount_games):
            print(i + 1)
            game_result = self.single_game()
            while game_result == -1:
                self.nmm = Game_NineMensMorris()
                game_result = self.single_game()
            if game_result == 1:
                self.white_wins += 1
            elif game_result == 2:
                self.black_wins += 1

            for board, rank in zip(run_games.nmm.states, run_games.nmm.state_scores):
                aggregated_dict[board]['total_rank'] += rank
                aggregated_dict[board]['count'] += 1

            board_ranks = {**existing_data,
                           **{board: [data['total_rank'] / data['count'], data['count']] for board, data in
                              aggregated_dict.items()}}

            unique_dict = {}
            for key, value in board_ranks.items():
                if key not in unique_dict:
                    unique_dict[key] = value
            board_ranks = unique_dict

            self.nmm = Game_NineMensMorris()

        with open('GameData.json', 'w') as file:
            json.dump(board_ranks, file, indent=4)

        print("Wins for white:", run_games.white_wins)
        print("Wins for black:", run_games.black_wins)

        print(time.time() - start_time, "seconds")

run_games = Games()
run_games.multiply_games()
