import random

import numpy as np

from models.Result import Result


#############################start_of_the_game_user_input_functions##################################
def is_against_computer():
    select_computer_or_human = '0'  # 0 - no choice yet, 1 - Other Player, 2 - Computer
    while select_computer_or_human not in ['1', '2']:
        try:
            select_computer_or_human = input(
                "Who would you like to play against?\n1 - Other Player\n2 - Computer\nYour choice: ")
            if select_computer_or_human not in ['1', '2']:
                raise Exception("Invalid choice, try another time.")
        except Exception as e:
            print(e)
    return select_computer_or_human == '2'
    # if the game is against computer the function returns True


def select_name(player_num, is_against_computer):
    name = ""
    if is_against_computer:
        player_num = "your" # no need to print player's number if it's only one player against the computer
    # validation - name isn't missing
    while name == "":
        try:
            name = input(f"Type {player_num} player's nick name: ")
            if len(name) < 1:
                raise Exception("Name is missing, please try again")
        except Exception as e:
            print(e)
    return name


def select_player_symbol(player_name, symbols_list):
    is_valid = False
    player_symbol = None
    print(f"Hello {player_name}!")
    while not is_valid:
        player_symbol = input(
            "select a symbol for your player: X / O\nFor random symbol - please press Enter\nYour symbol: ").upper().strip()
        # if the user click Enter - the symbol should be a random number
        if len(player_symbol) < 1:
            player_symbol = random.choice(symbols_list)
            print(f"{player_name}, your random symbol is '{player_symbol}'.")
            return player_symbol
        is_valid = player_symbol in symbols_list
    return player_symbol


############################boards_preparing###################################

def create_num_board():
    board = np.arange(1, 10).reshape(3, 3)
    return board


# num board for symbol location selection

def create_game_board(board_size):
    board = np.full(board_size, '-')
    return board


def print_board(board):
    for i in board:
        for j in i:
            print(j, end=" ")
        print()


def print_board_numbers(num_board):
    for i in num_board:
        for j in i:
            print(j, end=" ")
        print()


def print_game_instructions(board, num_board):
    print("Before we start - a small explanation:\nOn each turn you'll have to choose a cell from the board - ")
    print("Your game board:")
    print_board(board)
    input()
    print("On your turn - select cell by its number:")
    print_board_numbers(num_board)
    input()


# for convenience - during the game we'll use a function that shows both number and regular board:
def print_boards(board, num_board):
    for row_1, row_2 in zip(board, num_board):
        for elem_1 in row_1:
            print(elem_1, end=" ")
        print(end="     ")
        for elem_2 in row_2:
            print(elem_2, end=" ")
        print()


###############################################################

# convert the player's number selection to the relevant indexes on the board
def convert_num_to_indexes(location_num, num_board):
    for row_index in range(len(num_board)):
        for param_index in range(len(num_board[row_index])):
            if num_board[row_index][param_index] == location_num:
                return (row_index, param_index)


def is_cell_free(row_index, column_index, board):
    return board[row_index, column_index] == '-'


def select_number(player_name, player_symbol):
    is_valid = False
    location_num = None
    while not is_valid:
        try:
            location_num = int(input(f"{player_name} - select cell location for {player_symbol}: "))
            if not 1 <= location_num <= 9:
                raise Exception
            is_valid = True
        except Exception:
            print("Invalid choice, try another time")
    return location_num


def update_board(row_index, column_index, player_symbol, board): # put the symbol on the selected location on board
    board[row_index, column_index] = player_symbol


def select_random_computer_indexes(board):
    indexes_options = []
    for row_i, row_v in enumerate(board):
        for elem_i, elem_v in enumerate(row_v):
            if elem_v == "-":
                indexes_options.append((row_i, elem_i))
                # adding only the indexes which their cell is empty to the computer options
    chosen_indexes = random.choice(indexes_options)
    row_index = chosen_indexes[0]
    column_index = chosen_indexes[1]
    return row_index, column_index


def play_turn(player_name, player_symbol, num_board, board, is_computer_turn):
    if is_computer_turn:
        print("Computer's turn:")
        row_index, column_index = select_random_computer_indexes(board)
    else:
        cell_free = False
        while not cell_free:
            selected_num = select_number(player_name, player_symbol)
            row_index, column_index = convert_num_to_indexes(selected_num, num_board)
            cell_free = is_cell_free(row_index, column_index, board)
            if not cell_free:
                print("this cell is taken! please select another cell")
    update_board(row_index, column_index, player_symbol, board)
    print_boards(board, num_board)


def is_winner(board, player_symbol):
    for i in board:
        if i[0] == i[1] == i[2] == player_symbol:
            return True  # winning by row identical symbols
    for i in board:
        for j_index in range(len(i)):
            if board[0][j_index] == board[1][j_index] == board[2][j_index] == player_symbol:
                return True # winning by column identical symbols
            elif board[0][0] == board[1][1] == board[2][2] == player_symbol or board[0][2] == board[1][1] == board[2][0] == player_symbol:
                return True  # winning by diagonal line identical symbols
        else:
            return False


def is_board_full(board):
    for i in board:
        for j in i:
            if j == '-':
                return False
    return True


def get_result(board, player_A_symbol, player_B_symbol):
    if is_winner(board, player_A_symbol):
        return Result.PLAYER_A
    elif is_winner(board, player_B_symbol):
        return Result.PLAYER_B
    elif is_board_full(board): #if there is no winner and the board is full, the result is a tie.
        return Result.TIE
    else:
        return Result.NO_RESULT_YET


def print_results(result, player_A_name, player_B_name):
    if result == Result.PLAYER_A:
        print(f"*******************\n{player_A_name} is the winner!\n*******************")
    if result == Result.PLAYER_B:
        print(f"*******************\n{player_B_name} is the winner!\n*******************")
    if result == Result.TIE:
        print("*******************\nIt's a tie!\n*******************")


def is_another_game():
    another_game = None
    while another_game not in ['y', 'n']:
        try:
            another_game = input("Would you like to play another game? select y/n\nYour choice: ").strip().lower()
            if another_game not in ['y', 'n']:
                raise Exception("invalid choice - try again:")
        except Exception as e:
            print(e)
    return another_game == 'y'
