# Modules/Project files
from Settings import *
import random
import math
import time

# Constants
PLAYER_PIECE = BLUE + "O" + END_COLOR
OPPONENT_PIECE = RED + "X" + END_COLOR

MAX_MOVES = 9
WINNING_LINES = (
    # Horizontal
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    # Vertical
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    # Diagonal
    (0, 4, 8), (2, 4, 6))


# Print rules
def explain_rules(user):
    # Print welcome statement
    print(BLUE + "\n\n" + "WELCOME TO TIC TAC TOE ".center(LINE_WIDTH))
    print("\n" + user.center(LINE_WIDTH) + END_COLOR)
    # Rules
    print(MAGENTA + "\n" + "Players take turns placing one piece within a 3 by 3 grid each turn.".center(LINE_WIDTH))
    print("\n" + "The aim of the game is to get 3 pieces of the same player aligned.".center(LINE_WIDTH))
    print("\n" + "The line formed can be diagonal, horizontal or vertical.".center(LINE_WIDTH))
    print("\n" + "If such line is formed, the player whose aligned pieces belongs to wins.".center(LINE_WIDTH))
    print("\n" + "If all the grid spaces have been taken and no lines are formed, the game is a draw."
          .center(LINE_WIDTH)
          + END_COLOR + "\n")


# Function to display board
def display_board(grid_spaces):
    # First grid line
    print("\n" + " _______________________ ".center(LINE_WIDTH))
    print("|       |       |       |".center(LINE_WIDTH))
    # Value line
    print(("|   {}   |   {}   |   {}   |".format(grid_spaces[0], grid_spaces[1], grid_spaces[2]))
          # Set length of each row with values accordingly
          # colored text takes up 9 characters, so to ensure entire line is centered, length must be found
          .center((LINE_WIDTH - len(" " * 3)) + len(grid_spaces[0]) + len(grid_spaces[1]) + len(
                   grid_spaces[2])))
    print("|_______|_______|_______|".center(LINE_WIDTH))
    # Second grid line
    print("|       |       |       |".center(LINE_WIDTH))
    # Value line
    print(("|   {}   |   {}   |   {}   |".format(grid_spaces[3], grid_spaces[4], grid_spaces[5]))
          # Set length of each row with values accordingly
          .center((LINE_WIDTH - len(" " * 3)) + len(grid_spaces[3]) + len(grid_spaces[4]) + len(
                   grid_spaces[5])))

    print("|_______|_______|_______|".center(LINE_WIDTH))
    # Third grid line
    print("|       |       |       |".center(LINE_WIDTH))
    # Value line
    print(("|   {}   |   {}   |   {}   |".format(grid_spaces[6], grid_spaces[7], grid_spaces[8]))
          # Set length of each row with values accordingly
          .center((LINE_WIDTH - len(" " * 3)) + len(grid_spaces[6]) + len(grid_spaces[7]) + len(
                   grid_spaces[8])))
    print("|_______|_______|_______|".center(LINE_WIDTH) + "\n")


# Check game end criteria
def pos_eval(grid_spaces):
    # Set initial game_over value to draw when result is not determined
    game_result = [0, "Draw"]

    # Check if wins occur
    for j in range(len(WINNING_LINES)):
        if grid_spaces[WINNING_LINES[j][0]] == OPPONENT_PIECE and \
                grid_spaces[WINNING_LINES[j][1]] == OPPONENT_PIECE and \
                grid_spaces[WINNING_LINES[j][2]] == OPPONENT_PIECE:
            game_result = [1, "Won"]
        elif grid_spaces[WINNING_LINES[j][0]] == PLAYER_PIECE and \
                grid_spaces[WINNING_LINES[j][1]] == PLAYER_PIECE and \
                grid_spaces[WINNING_LINES[j][2]] == PLAYER_PIECE:
            game_result = [-1, "Won"]

    # Check if not draw
    if game_result[1] != "Won":
        for space in grid_spaces:
            if space == " ":
                game_result = [0, "Unknown"]
                break

    # Return final game result and piece to determine for which player
    return game_result


# Find empty space between two pieces within a winning line
def take_or_block_win(grid_spaces, piece):
    # For loop to check condition of each line
    for k in range(len(WINNING_LINES)):
        # reset piece count every cycle
        piece_count = 0
        # reset empty_space_position every cycle
        empty_space_position = 0

        # Second for loop to check values for each quadrant
        for space in WINNING_LINES[k]:
            # Check whether quadrant value matches piece
            if grid_spaces[space] == piece:
                # Increase piece count by one if quadrant values match
                piece_count += 1
            # Check whether quadrant value matches space
            elif grid_spaces[space] == " ":
                # Store empty space position (+1 as 1 is taken away from move later)
                empty_space_position = space + 1

            # If there are at least 2 of the same pieces and one empty space within a line,
            # make move as position of empty space to either block or take a win
            if piece_count == 2 and empty_space_position != 0:
                # Update move as empty space position and return it
                move = empty_space_position

                return move

    # If no wins nor blocks are detected, return nothing
    return "N/A"


# Get players move
def get_player_move(grid_spaces, user):
    # Initiate variable
    move = None

    # Input loop
    asking = True
    while asking:
        # Set error_statement
        error_statement = None

        # Player turn statement
        print(BLUE + "\n" + ("...... " + user + "'s Turn (O) ......")
              .center(LINE_WIDTH) + "\n" + END_COLOR)

        # Move
        move = get_input(["Enter the position you want to place a piece (Left Top is 1, Mid Top is 2 and so on)"],
                         True, False, False, True)

        if move is not None:
            # Position within grid
            if 10 > move > 0:
                # If move does not collide with any other pieces, break loop
                if grid_spaces[move - 1] == " ":
                    break
                else:
                    error_statement = "ERROR: You cannot place a piece where there is already another."
            else:
                error_statement = "Please enter a square between 1 and 9"

        # Show error message if error occurs
        if error_statement is not None:
            print(GREEN + error_statement.center(LINE_WIDTH) + END_COLOR + "\n")
        time.sleep(1)
        display_board(grid_spaces)

    # Return given move/grid number
    return move


# Get easy computers move
def get_easy_computer_move(grid_spaces, computer):
    # Print computer's turn statement
    print(RED + "\n" + ("...... " + computer + "'s Turn (X) ......")
          .center(LINE_WIDTH) + "\n" + END_COLOR)

    # Initiate variable
    move = None
    # Loop until acceptable move is generated
    generating = True
    while generating:
        move = random.randint(1, 9)
        # If move does not collide with any pieces, break
        if grid_spaces[move - 1] == " ":
            generating = False

    # Return generated move
    return move


# Get medium computers move
def get_medium_computer_move(grid_spaces, computer):
    # Print computer's turn statement
    print(RED + "\n" + ("...... " + computer + "'s Turn (X) ......")
          .center(LINE_WIDTH) + "\n" + END_COLOR)

    # Take wins
    move = take_or_block_win(grid_spaces, OPPONENT_PIECE)
    # If no wins are available, check to block any player wins
    if move == "N/A":
        # Block wins
        move = take_or_block_win(grid_spaces, PLAYER_PIECE)
        # Else randomise move (same with easy computer)
        if move == "N/A":
            # Initiate variable
            move = None
            # Loop until acceptable move is generated
            generating = True
            while generating:
                move = random.randint(1, 9)
                # If move does not collide with any pieces, break
                if grid_spaces[move - 1] == " ":
                    generating = False
    # Return final move
    return move


# Get hard computers move
def get_hard_computer_move(grid_spaces, computer):
    # Print computer's turn statement
    print(RED + "\n" + ("...... " + computer + "'s Turn (X) ......")
          .center(LINE_WIDTH) + "\n" + END_COLOR)

    # return best move from minimax function
    return minimax_recursion(grid_spaces, True, 0, random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9))[1]


# Minimax function for hard computer move
def minimax_recursion(grid_spaces, opponent_turn, depth, space_order):
    # Set best move
    best_move = None
    # Set min depth (represents least moves required to achieve a certain evaluation)
    min_depth = math.inf

    # Get evaluation of current position
    current_position_result = pos_eval(grid_spaces)
    # Base case (Game is over)
    if current_position_result[1] == "Won" or current_position_result[1] == "Draw":
        return [current_position_result[0], depth], best_move

    # opponent's turn
    elif opponent_turn:
        # Set maximum score for opponent (set to worse possible score for opponent)
        maximum_score = -math.inf

        # Space order is shuffled to increase randomness of move
        for i in space_order:
            # Find all possible next moves
            if grid_spaces[i] == " ":
                child_position = grid_spaces[:]
                child_position[i] = OPPONENT_PIECE

                # Check best evaluation for every next position possible
                # Check depth(moves) required to reach the best evaluation
                child_position_evaluation, child_depth = minimax_recursion(child_position, False, depth + 1,
                                                                           space_order)[0]
                # Update max score and min_depth if evaluation is better for opponent or
                # same score can be achieved with lesser moves
                if maximum_score < child_position_evaluation or \
                        (maximum_score == child_position_evaluation and child_depth <= min_depth):
                    maximum_score = child_position_evaluation
                    min_depth = child_depth
                    best_move = i + 1

        # Best move, evaluation and min_depth returned for opponent among all moves calculated
        return [maximum_score, min_depth], best_move

    # Player's turn
    elif not opponent_turn:
        # Set minimum score for player (worse possible score)
        minimum_score = math.inf

        # Space order is shuffled to increase randomness of move
        for i in space_order:
            # Find all possible next moves
            if grid_spaces[i] == " ":
                child_position = grid_spaces[:]
                child_position[i] = PLAYER_PIECE

                # Check best evaluation for every next position possible
                # Check depth(moves) required to reach the best evaluation
                child_position_evaluation, child_depth = minimax_recursion(child_position, True, depth + 1,
                                                                           space_order)[0]
                # Update min score and min_depth if evaluation is better for opponent or
                # same score can be achieved with lesser moves
                if minimum_score > child_position_evaluation or \
                        (minimum_score == child_position_evaluation and child_depth <= min_depth):
                    minimum_score = child_position_evaluation
                    min_depth = child_depth
                    best_move = i + 1

        # Best move, evaluation and min_depth for player among all moves calculated
        return [minimum_score, min_depth], best_move


# Get opponent choice
def opponent_choice():
    # Initiate variables
    choice = None

    # Loop until choice given
    inserting = True
    while inserting:
        # Set error_statement
        error_statement = None

        # Opponent choice
        choice = get_input(["Choose your opponent: PLAYER(P) COMPUTER(C)"])

        # Computer
        if choice == "computer" or choice == "c":
            choice = get_input(["Choose computer difficulty: EASY(E) MEDIUM(M) HARD(H)"], True, False)

            # Check difficulty validity and reformat
            if choice == "easy" or choice == "e":
                choice = "easy computer"
                inserting = False
            elif choice == "medium" or choice == "m":
                choice = "medium computer"
                inserting = False
            elif choice == "hard" or choice == "h":
                choice = "hard computer"
                inserting = False
            # Error statement
            elif choice is not None:
                error_statement = "ERROR: Please enter 'EASY(E)', 'MEDIUM(M)' or 'HARD(H)'."
        # Choice player
        elif choice == "player" or choice == "p":
            get_name = True
            while get_name:
                choice = get_input(["Enter player 2's name"], False).strip().title()
                confirm = get_input(["Confirmed? (Y/N)"], True, True, True)
                if confirm == "y":
                    get_name = False
                    inserting = False
        # Error statement
        elif choice is not None:
            error_statement = "ERROR: Please enter either 'Player' or 'Computer' for your opponent choice."

        if error_statement is not None:
            print(GREEN + error_statement.center(LINE_WIDTH) + "\n" + END_COLOR)

    # Return opponent choice
    return choice


# Main Game Function
def tic_tac_toe(name):
    # Rules
    explain_rules(name)

    # Initialising scores
    player_to_player_2_score = [0, 0]
    player_to_easy_computer_score = [0, 0]
    player_to_medium_computer_score = [0, 0]
    player_to_hard_computer_score = [0, 0]

    # Game loop
    playing = "y"
    while playing == "y" or playing == "yes":
        # Set variables
        grid = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        result = None

        # Get opponent choice
        opponent = opponent_choice()

        # Display board
        display_board(grid)

        # Determine opponent score
        if opponent == "easy computer":
            player_to_opponent_score = player_to_easy_computer_score
        elif opponent == "medium computer":
            player_to_opponent_score = player_to_medium_computer_score
        elif opponent == "hard computer":
            player_to_opponent_score = player_to_hard_computer_score
        else:
            player_to_opponent_score = player_to_player_2_score

        # Randomise turn
        turn = random.choice(["player", "opponent"])

        # Loop for all grid spaces
        for _ in range(MAX_MOVES):
            # Player turn
            if turn == "player":
                # Get move
                player_move = get_player_move(grid, name)
                # Enter move to grid
                grid[player_move - 1] = PLAYER_PIECE

                # Change turn
                turn = "opponent"
            # Opponent turn
            elif turn == "opponent":
                # Get move depending on opponent
                # Computers
                if opponent == "easy computer":
                    opponent_move = get_easy_computer_move(grid, opponent.title())
                elif opponent == "medium computer":
                    opponent_move = get_medium_computer_move(grid, opponent.title())
                elif opponent == "hard computer":
                    opponent_move = get_hard_computer_move(grid, opponent.title())
                # Player
                else:
                    opponent_move = get_player_move(grid, opponent.title())
                # Enter move to grid
                grid[opponent_move - 1] = OPPONENT_PIECE

                # Change turn
                turn = "player"

            # Delay
            time.sleep(1)

            # Display updated board
            display_board(grid)

            # Check result
            result = pos_eval(grid)
            # Quit loop if one side has won
            if result[1] == "Won":
                break

        # Delay
        time.sleep(1)

        # Update scores from result
        # Win
        if result[1] == "Won":
            # Add 1 point to winner
            # Player is minimising player, -1 represents win for player
            if result[0] == -1:
                # Player win statement
                game_over_text = "{} has {}!".format(name, result[1])
                print(MAGENTA + "\n" + game_over_text.center(LINE_WIDTH) + END_COLOR)

                player_to_opponent_score[0] += 1
            # Opponent win
            else:
                # Opponent win statement
                game_over_text = "{} has {}!".format(opponent.title(), result[1])
                print(MAGENTA + "\n" + game_over_text.center(LINE_WIDTH) + END_COLOR)

                player_to_opponent_score[1] += 1

        # Draw
        else:
            # Draw statement
            game_over_text = "It is a draw!"
            print(MAGENTA + "\n" + game_over_text.center(LINE_WIDTH) + END_COLOR)

            player_to_opponent_score[0] += 0.5
            player_to_opponent_score[1] += 0.5

        # Delay
        time.sleep(0.5)

        # Print current score
        print(MAGENTA + "\n" + ("The current score between " + name + " and " + opponent.title() + " is")
              .center(LINE_WIDTH))
        print((str(player_to_opponent_score[0]) + " : " + str(player_to_opponent_score[1])).center(LINE_WIDTH) +
              END_COLOR + "\n")

        # Delay
        time.sleep(1)

        # Ask user if user wants to play another game
        playing = get_input(["Play again? (Y/N)"], True, True, True)


# Game (Run if individual)
if __name__ == "__main__":
    # Game function
    tic_tac_toe(ask_name())
