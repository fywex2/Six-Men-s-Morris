import random

# Board representation
board = [[' ' for _ in range(7)] for _ in range(7)]

# Player symbols
player1_symbol = 'X'
player2_symbol = 'O'

# Function to print the board
def print_board():
    for row in board:
        print("|" + "|".join(row) + "|")

# Function to check if a move is valid
def is_valid_move(board, player, row, col):
    if row < 0 or row > 6 or col < 0 or col > 6:
        return False
    if board[row][col] != ' ':
        return False
    if player.count_pieces() == 9:  # Placement phase
        return True
    else:  # Movement phase
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i <= 6 and 0 <= col + j <= 6 and board[row + i][col + j] == player.symbol:
                    if abs(i) + abs(j) == 2:  # Adjacent position
                        return True
                    elif abs(i) + abs(j) == 3 and board[(row + row + i) // 2][(col + col + j) // 2] == player.symbol:  # Mill jump
                        return True
    return False

# Function to place a player's piece on the board
def place_piece(board, player, row, col):
    board[row][col] = player.symbol

# Function to remove a player's piece from the board
def remove_piece(board, row, col):
    board[row][col] = ' '

# Function to check for a winner
def check_winner(board):
    for i in range(7):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
        if i == 0 or i == 3 or i == 6:
            if board[i][0] == board[4][i] == board[8 - i][8 - i] != ' ':
                return board[i][0]
            if board[0][i] == board[i][4] == board[8 - i][8 - i] != ' ':
                return board[0][i]
    return None

# Class to represent a player
class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        self.pieces = []

    def count_pieces(self):
        return len(self.pieces)

    def get_possible_moves(self, board):
        possible_moves = []
        for row in range(7):
            for col in range(7):
                if is_valid_move(board, self, row, col):
                    possible_moves.append((row, col))
        return possible_moves

    def make_random_move(self, board):
        possible_moves = self.get_possible_moves(board)
        if possible_moves:
            row, col = random.choice(possible_moves)
            place_piece(board, self, row, col)
            self.pieces.append((row, col))
            return True
        else:
            return False

# Main game loop
player1 = Player(player1_symbol)
player2 = Player(player2_symbol)
current_player = player1

while True:
    print_board()

    if not current_player.make_random_move(board):
        print("Player", current_player.symbol, "has no valid moves.")
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1
        continue

def main():
    player1 = Player(player1_symbol)
    player2 = Player(player2_symbol)
    current_player = player1

while True:
    print_board()

    if not current_player.make_random_move(board):
        print("Player", current_player.symbol, "has no valid moves.")
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1
        continue

    winner = check_winner(board)
    if winner:
        print("Player", winner, "wins!")
        break

# Code to execute the game
if __name__ == "__main__":
    main()  # Call the main game loop

    # Announce the winner
    winner = check_winner(board)
    if winner == player1_symbol:
        print("Black wins!")
    elif winner == player2_symbol:
        print("White wins!")
    else:
        print("It's a draw!")