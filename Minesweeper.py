# Modules/Project files
from Settings import *
import random
import time


# Constants
# Position/Coordinates
ALPHA_CORDS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
NUM_CORDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

# Symbols
BOMB = RED + "X" + END_COLOR
FLAG = YELLOW + "F" + END_COLOR


# Explain rules
def explain_rules(user):
    # Welcome statement
    print(BLUE + "\n\n" + "WELCOME TO MINESWEEPER".center(LINE_WIDTH))
    print("\n" + user.center(LINE_WIDTH) + END_COLOR)
    # Rules
    print(MAGENTA + "\n" + "The objective of the game is to clear a rectangular board".center(LINE_WIDTH))
    print("\n" + "containing hidden 'mines' or bombs without detonating any of them".center(LINE_WIDTH))
    print("\n" + "For each move, a value of a space can be revealed, either a number or a mine.".center(LINE_WIDTH))
    print("\n" + "A number in a space represents the number of neighbouring mines horizontally, vertically and diagonally around it.".center(LINE_WIDTH))
    print("\n" + "Spaces can be flagged to indicate a mine at that position to prevent accidentally opening of a mine".center(LINE_WIDTH))
    print("\n" + "When all the spaces are revealed, the player wins.".center(LINE_WIDTH))
    print("\n" + "If a mine is revealed, the game is a loss.".center(LINE_WIDTH) + "\n" + END_COLOR)


# Print board
def show_board(spaces):
    # Space/Line break and top part of section
    print("\n" + "       _______ _______ _______ _______ _______ _______ _______ _______ _______ _______ ".center(LINE_WIDTH))

    # Loop through each horizontal line and display each line
    # (From last line to first line backwards from sections list since numbers are in decreasing order)
    for line in range(len(spaces), 0, -1):
        # Set actual line value
        line -= 1
        # Line 1 (top)
        print("      |       |       |       |       |       |       |       |       |       |       |".center(LINE_WIDTH))
        # Line 2 (value line/middle)
        print("{}    |   {}   |   {}   |   {}   |   {}   |   {}   |   {}   |   {}   |   {}   |   {}   |   {}   |"
              .format(CYAN + NUM_CORDS[line] + END_COLOR, spaces[line][0], spaces[line][1], spaces[line][2],
                      spaces[line][3], spaces[line][4], spaces[line][5], spaces[line][6], spaces[line][7],
                      spaces[line][8], spaces[line][9])
              .center((LINE_WIDTH - 10) + len(CYAN + END_COLOR) + len(spaces[line][0]) + len(spaces[line][1]) + len(
               spaces[line][2]) + len(spaces[line][3]) + len(spaces[line][4]) + len(spaces[line][5]) + len(
               spaces[line][6]) + len(spaces[line][7]) + len(spaces[line][8]) + len(spaces[line][9])))
        # Line 3 (cover)
        print("      |_______|_______|_______|_______|_______|_______|_______|_______|_______|_______|".center(LINE_WIDTH))

    # Space/Line break and add alpha cords
    print(CYAN + "\n" +
          ("             {}       {}       {}       {}       {}       {}       {}       {}       {}       {}       "
           .format(ALPHA_CORDS[0].upper(), ALPHA_CORDS[1].upper(), ALPHA_CORDS[2].upper(), ALPHA_CORDS[3].upper(),
                   ALPHA_CORDS[4].upper(), ALPHA_CORDS[5].upper(), ALPHA_CORDS[6].upper(), ALPHA_CORDS[7].upper(),
                   ALPHA_CORDS[8].upper(), ALPHA_CORDS[9].upper())).center(LINE_WIDTH) + "\n" + END_COLOR)


# Create puzzle grid
def create_puzzle(spaces, level):
    # Generating the bombs according to difficulty
    if level == "easy" or level == "e":
        num_bombs = random.randint(5, 15)
    elif level == "medium" or level == "m":
        num_bombs = random.randint(16, 25)
    else:
        num_bombs = random.randint(26, 35)

    # Plant bombs
    for _ in range(num_bombs):
        # Loop until a bomb is planted in a valid space
        planting = True
        while planting:
            # Randomise position and plant
            random_pos = random.randint(0, 9), random.randint(0, 9)
            # Ensure bombs aren't repeatedly planted at same square
            if spaces[random_pos[0]][random_pos[1]] != BOMB:
                spaces[random_pos[0]][random_pos[1]] = BOMB
                planting = False

    # Put numbers/empty spaces
    for i in range(len(spaces)):
        for j in range(len(spaces[i])):
            if spaces[i][j] != BOMB:
                # Set Bomb Count
                bomb_count = 0
                # Loop through all neighbour squares and count number of bombs
                for pos in find_neighbours([i, j]):
                    if spaces[pos[0]][pos[1]] == BOMB:
                        bomb_count += 1

                # Update space with number of bombs around it (dash '-' for empty square)
                if bomb_count == 0:
                    spaces[i][j] = "-"
                else:
                    spaces[i][j] = str(bomb_count)


# Find squares around a square
def find_neighbours(square_pos):
    # Set neighbour square positions list
    neighbour_squares = []

    # Loop for all neighbouring squares positions
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Set positions
            horizontal_pos = square_pos[0] + i
            vertical_pos = square_pos[1] + j

            # Indexes between 0 and 9
            if 0 <= horizontal_pos <= 9 and 0 <= vertical_pos <= 9:
                neighbour_squares.append([horizontal_pos, vertical_pos])

    # Final list (including given position)
    return neighbour_squares


# Open/Flag space
def get_action(shown_spaces, solution_spaces):
    # Setting variables
    pos = None
    action = None

    # Input loop
    inserting = True
    while inserting:
        # Set error statement
        error_statement = None

        # Chosen position
        pos = get_input(["Enter the position you wish to open/flag (format: row + column, eg: Top Left square is A10)"],
                        True, False)

        if pos is not None:
            if len(pos) != 2 and len(pos) != 3:
                error_statement = "ERROR: Please enter a valid coordinate."
            elif pos[0] not in ALPHA_CORDS or pos[1:] not in NUM_CORDS:
                error_statement = "ERROR: Please enter a valid coordinate."
            else:
                # Convert ALPHA and NUM pos to grid index format
                pos = [NUM_CORDS.index(pos[1:]), ALPHA_CORDS.index(pos[0])]

                # Input repeated (position already opened)
                if shown_spaces[pos[0]][pos[1]] != " " and shown_spaces[pos[0]][pos[1]] != FLAG:
                    error_statement = "ERROR: You cannot take action on an already opened section."
                # Valid
                else:
                    # Action
                    action = get_input(["Do you want to flag/unflag the section or open it?",
                                        "('F' for flag/unflag and press 'ENTER' to open)"], True, False, False, False, True)

                    # Input on flagged square
                    if action == "" and shown_spaces[pos[0]][pos[1]] == FLAG:
                        error_statement = "ERROR: You cannot open a flagged square (To open this square, unflag it first)."
                    # Input valid
                    elif action == "" or action == "f" or action == "flag":
                        break
                    # Input not according to format
                    else:
                        error_statement = "ERROR: Please enter 'F' for flag/unflag or press enter to open."

        if error_statement is not None:
            print(GREEN + error_statement.center(LINE_WIDTH) + "\n" + END_COLOR)
        time.sleep(1)
        show_board(shown_spaces)

    # Set list of positions affected
    pos_list = [pos]
    # Bomb opened
    if solution_spaces[pos[0]][pos[1]] == BOMB:
        # All positions should be opened if bomb is uncovered
        if action == "":
            for i in range(len(solution_spaces)):
                for j in range(len(solution_spaces[i])):
                    pos_list.append([i, j])
            # Change action to 'Bomb' to indicate a bomb revealed
            action = "Bomb"
    else:
        # Use recursion to find all squares to take action (including squares around empty squares)
        if action == "":
            get_connecting_squares(pos, pos_list, solution_spaces)

    # Affected positions and action taken
    return pos_list, action


# Recursion to find all squares around empty squares and append to list
def get_connecting_squares(given_pos, pos_list, answer_spaces):
    for positions in find_neighbours(given_pos):
        if answer_spaces[positions[0]][positions[1]] == "-":
            for sub_pos in find_neighbours(positions):
                if sub_pos not in pos_list:
                    pos_list.append(sub_pos)
                    get_connecting_squares(sub_pos, pos_list, answer_spaces)


# Game Function
def minesweeper(name):
    # Rules
    explain_rules(name)
    # Set score (number of puzzles solved)
    num_solved = 0

    # Game loop
    playing = "y"
    while playing == "y" or playing == "yes":
        # Set actual spaces
        puzzle_sections = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]
        # Set visual/shown spaces
        shown_sections = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                          [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

        # Set result
        result = None

        # Create puzzle
        create_puzzle(puzzle_sections, get_level())

        # In game loop
        in_game = True
        while in_game:
            # Display grid
            show_board(shown_sections)

            # If result has been determined (game ended), quit loop
            if result is not None:
                in_game = False
                continue

            # Ask for a position and an action
            chosen_sections, action = get_action(shown_sections, puzzle_sections)
            # Update shown grid with all affected squares
            for pos in chosen_sections:
                # Flag
                if action == "Flag" or action == "f":
                    # Remove
                    if shown_sections[pos[0]][pos[1]] == FLAG:
                        shown_sections[pos[0]][pos[1]] = " "
                    # Add
                    else:
                        shown_sections[pos[0]][pos[1]] = FLAG
                # Open
                else:
                    shown_sections[pos[0]][pos[1]] = puzzle_sections[pos[0]][pos[1]]

            # Check if Lost
            if action == "Bomb":
                result = "Lost"
            # Check if Won
            else:
                full = True
                for i in range(len(shown_sections)):
                    for j in range(len(shown_sections[i])):
                        if shown_sections[i][j] != puzzle_sections[i][j] and puzzle_sections[i][j] != BOMB:
                            full = False
                if full:
                    # Fill all bombs unflagged with flags after all numbered sections are opened
                    for i in range(len(shown_sections)):
                        for j in range(len(shown_sections[i])):
                            if shown_sections[i][j] == " ":
                                shown_sections[i][j] = FLAG
                    # Update results and score
                    result = "Won"
                    num_solved += 1

        # Result statement
        result_statement = "******************** " + name + " has " + result + "!" + " ********************"
        num_solved_statement = "Solved puzzles: " + str(num_solved)
        print(MAGENTA + result_statement.center(LINE_WIDTH))
        print(num_solved_statement.center(LINE_WIDTH) + END_COLOR + "\n")

        # Ask for replay
        playing = get_input(["Play again? (Y/N)"], True, True, True)


# Game (Run if individual)
if __name__ == "__main__":
    # Game function
    minesweeper(ask_name())
