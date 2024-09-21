from functions import *
import time

from models.Result import Result

if __name__ == '__main__':
    input("Welcome to Tic-Tac-Toe game!")
    is_against_computer = is_against_computer()
    symbols_list = ['X', 'O']
    player_A_name = select_name("first", is_against_computer)
    player_A_symbol = select_player_symbol(player_A_name, symbols_list)
    print()

    #automatically select the symbol for the other player
    player_B_symbol = None
    for symbol in symbols_list:
        if symbol != player_A_symbol:
            player_B_symbol = symbol

    if is_against_computer:
        player_B_name = "Computer"
        input(f"{player_B_name}'s symbol is: {player_B_symbol}")
    else:
        player_B_name = select_name("second", is_against_computer)
        input(f"{player_B_name}, your symbol is '{player_B_symbol}'.")
        print()

    is_game_active = True
    first_game = True  # for instructions print
    while is_game_active:
        num_board = create_num_board()
        board = create_game_board((3, 3))
        if first_game:
            print_game_instructions(board, num_board)
        print("**************************")
        print("Lets Start Play!")
        print("**************************")
        print_boards(board, num_board)

        result = Result.NO_RESULT_YET
        player_A_turn = True # will change in each turn

        while result == Result.NO_RESULT_YET:
            # change the name and symbol according to the player that is now playing
            if player_A_turn:
                active_player_name = player_A_name
                active_symbol = player_A_symbol
                is_computer_turn = False  # player A is always the user (not computer)
            else:
                active_player_name = player_B_name
                active_symbol = player_B_symbol
                is_computer_turn = is_against_computer # if playing against computer, player B plays computer's turn
            if is_computer_turn:
                time.sleep(1.1) # postponing before computer's turn

            # the active player play his turn
            play_turn(active_player_name, active_symbol, num_board, board, is_computer_turn)
            # check the result
            result = get_result(board, player_A_symbol, player_B_symbol)
            if result != Result.NO_RESULT_YET: # print only is there's a result
                print_results(result, player_A_name, player_B_name)
                break
            player_A_turn = not player_A_turn # change between player's A and player's B turn

        first_game = False
        is_game_active = is_another_game() # if the player selects another game, the game stays active

    print("********************************************")
    print("The game is over! see you on the next time!")
    print("********************************************")
