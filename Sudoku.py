# Modules/Project files
from Settings import *
import random
import time


# Constants
# Coordinates
NUM_CORDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
ALPHA_CORDS = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

# Sudoku constants
TOTAL_SQUARES = 81
MIN_NUMBERS = 17


# Introduction
def explain_rules(user):
    """Prints introduction to game"""

    # Welcome statement
    print(BLUE + "\n\n" + "WELCOME TO SUDOKU".center(LINE_WIDTH))
    print("\n" + user.center(LINE_WIDTH) + "\n" + END_COLOR)
    # Rules
    print(MAGENTA + "\n" + "Sudoku is a single player game.".center(LINE_WIDTH))
    print("\n" + "Numbers 1 - 9 can be entered for each space.".center(LINE_WIDTH))
    print("\n" + "The objective is to fill a 9 × 9 grid with digits so that".center(LINE_WIDTH))
    print("\n" + "each column, each row, and each of the nine 3 × 3 sub-grids that compose the grid".center(LINE_WIDTH))
    print("\n" + "contain all of the digits from 1 to 9.".center(LINE_WIDTH) + "\n" + END_COLOR)


# Display grid
def display_grid(sections):
    """Displays sudoku grid in a graphical manner"""

    # Line break
    print("\n")

    # Show lines
    for line_count in range(len(sections)):
        # Calculate character length of line
        line_length = (LINE_WIDTH - (len(sections))) + len(CYAN + END_COLOR)
        for space_index in range(len(sections)):
            line_length += len(sections[line_count][space_index])

        # Split grid every 3 rows
        if line_count % 3 == 0:
            print("       _______ _______ _______   _______ _______ _______   _______ _______ _______ ".center(LINE_WIDTH))

        # Grid line with number coordinates
        print("      |       |       |       | |       |       |       | |       |       |       |".center(LINE_WIDTH))
        print((CYAN + f"{NUM_CORDS[-(line_count + 1)]}    " + END_COLOR +
               f"|   {sections[line_count][0]}   |   {sections[line_count][1]}   |   {sections[line_count][2]}   | "
               f"|   {sections[line_count][3]}   |   {sections[line_count][4]}   |   {sections[line_count][5]}   | "
               f"|   {sections[line_count][6]}   |   {sections[line_count][7]}   |   {sections[line_count][8]}   |")
              .center(line_length))
        print("      |_______|_______|_______| |_______|_______|_______| |_______|_______|_______|".center(LINE_WIDTH))

    # Alphabet coordinates
    print("\n" + CYAN +
          "          A       B       C         D       E       F         G       H       I    ".center(LINE_WIDTH)
          + END_COLOR + "\n")


# Get validity of position when a number is added
def grid_valid(sections, value, position,):
    """Checks validity of the grid if a new number is added"""

    # Match in horizontal lines
    for num in sections[position[0]]:
        if value == num or YELLOW + value + END_COLOR == num:
            return False

    # Match in vertical lines
    for line in sections:
        if value == line[position[1]] or YELLOW + value + END_COLOR == line[position[1]]:
            return False

    # Match in 3 x 3 grid
    grid_horizontal_num = ((position[0] // 3) + 1) * 3
    grid_vertical_num = ((position[1] // 3) + 1) * 3
    for h_pos in range(grid_horizontal_num - 3, grid_horizontal_num):
        for v_pos in range(grid_vertical_num - 3, grid_vertical_num):
            if value == sections[h_pos][v_pos] or YELLOW + value + END_COLOR == sections[h_pos][v_pos]:
                return False

    # Grid is valid if no matches are found
    return True


# Generate answer of puzzle
def solve_puzzle(puzzle_sections, solving):
    """
    Solves an incomplete sudoku grid
    If an invalid sudoku puzzle is given, the invalid puzzle is returned
    """

    # Loop through all spaces
    for i in range(len(puzzle_sections)):
        for j in range(len(puzzle_sections[i])):
            # Try numbers for empty spaces
            if puzzle_sections[i][j] == " ":
                # Randomise order of numbers to try for randomised solutions
                for num in random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 9):
                    # Enter number in grid if it is valid
                    if grid_valid(puzzle_sections, num, [i, j]):
                        # Colored numbers if solving for answer and white numbers for creating puzzle
                        if solving:
                            puzzle_sections[i][j] = YELLOW + num + END_COLOR
                        else:
                            puzzle_sections[i][j] = num
                        # Grid solved/end recursion
                        if solve_puzzle(puzzle_sections, solving):
                            return True
                        # Set space to empty and try different number if grid is unable to be solved
                        else:
                            puzzle_sections[i][j] = " "
                # All numbers are not valid
                return False
    # Grid filled/solved
    return True


# Create puzzle
def create_puzzle(sections, difficulty):
    """Creates a valid sudoku puzzle"""

    # To generate a valid sudoku puzzle, a valid solution must first be formed.
    solve_puzzle(sections, False)

    # Determine amount of numbers in puzzle
    num_numbers = None
    if difficulty == "easy":
        num_numbers = random.randint(MIN_NUMBERS + 26, MIN_NUMBERS + 35)
    elif difficulty == "medium":
        num_numbers = random.randint(MIN_NUMBERS + 16, MIN_NUMBERS + 25)
    elif difficulty == "hard":
        num_numbers = random.randint(MIN_NUMBERS + 5, MIN_NUMBERS + 15)

    # Calculate numbers to remove
    num_removed = TOTAL_SQUARES - num_numbers
    for i in range(num_removed):
        # Remove numbers loop
        removing = True
        while removing:
            random_position = random.randint(0, 8), random.randint(0, 8)
            if sections[random_position[0]][random_position[1]] != " ":
                sections[random_position[0]][random_position[1]] = " "
                removing = False


# Edit grid
def edit_input(sections):
    """Acquires a valid position and value to edit on the grid"""

    # Set variables
    position = None
    value = None

    # Input loop
    inserting = True
    while inserting:
        # Set error statement
        error_statement = None

        # Position/Solution
        position = get_input(["Choose a square (format: column + row, eg: top left square is A9 and bottom right square is I1)",
                              "Enter 'Answer(A) for the solution/to quit."], True, False)

        # No error in get_input
        if position is not None:
            # Solution needed
            if position == "answer" or position == "a":
                break
            # Invalid position
            elif len(position) != 2:
                error_statement = "ERROR: Please enter a valid coordinate or 'Answer(A)'."
            elif position[0] not in ALPHA_CORDS or position[1] not in NUM_CORDS:
                error_statement = "ERROR: Please enter a valid coordinate or 'Answer(A)'."
            else:
                # Reformat to list form
                position = [-(NUM_CORDS.index(position[1]) + 1), ALPHA_CORDS.index(position[0])]

                # Puzzle overwritten
                if sections[position[0]][position[1]] != " " and YELLOW not in sections[position[0]][position[1]]:
                    error_statement = "ERROR: You cannot change the original puzzle"

                # Valid
                else:
                    # Value/Number
                    value = get_input(["Enter a number from 1 to 9 for the square or press 'ENTER' to clear value in square."],
                                      True, False, False, True, True)

                    # Clear space
                    if value == "":
                        value = " "
                        break
                    # Number entered
                    elif value is not None:
                        # Not between 0 to 9
                        if 1 > value or value > 9:
                            error_statement = "ERROR: Please enter a number between 1 to 9"
                        # Valid
                        else:
                            # Change to string form
                            value = str(value)
                            break

        # If error occurs, show message and redisplay screen
        if error_statement is not None:
            print(GREEN + error_statement.center(LINE_WIDTH) + END_COLOR + "\n")
        time.sleep(1)
        display_grid(sections)

    # Converted position and number
    return position, value


# Main game
def sudoku(name):
    """Main game function to run game"""

    # Program loop
    playing = "y"
    while playing == "y" or playing == "yes":
        # Intro and rules
        explain_rules(name)

        # Set variables
        solved = False
        solution_given = False
        num_solved = 0

        grid = [[" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

        # Create random puzzle
        create_puzzle(grid, get_level())

        # Game loop
        in_game = True
        while in_game:
            # Display grid
            display_grid(grid)

            # Puzzle solved/solution given
            if solved or solution_given:
                # Display game end messages
                if solved:
                    print(MAGENTA + "\n" +
                          ("******************** CONGRATULATIONS " + name + "! Puzzle solved. ********************")
                          .center(LINE_WIDTH) + END_COLOR)
                    # Update score
                    num_solved += 1
                else:
                    print(MAGENTA + "Solved with Answer".center(LINE_WIDTH))
                # Display score
                print(MAGENTA +
                      ("Puzzles " + name + " has solved: " + str(num_solved)).center(LINE_WIDTH)
                      + END_COLOR + "\n")
                break

            # Position and value chosen
            pos, num = edit_input(grid)
            # Solution
            if pos == "answer" or pos == "a":
                # Reset grid to puzzle position
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        if YELLOW in grid[i][j]:
                            grid[i][j] = " "
                # Solve and update variables
                solve_puzzle(grid, True)
                solution_given = True
            # Edit grid
            else:
                grid[pos[0]][pos[1]] = YELLOW + num + END_COLOR

                # Check solved
                solved = True
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        value = grid[i][j]
                        grid[i][j] = " "
                        if not grid_valid(grid, value, [i, j]):
                            solved = False

                        grid[i][j] = value
                    
        # Replay/Quit
        playing = get_input(["Play again? (Y/N)"], True, True, True)


# Run Game individually
if __name__ == "__main__":
    sudoku(ask_name())
