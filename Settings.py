# Modules
import ctypes

# Constants
# Line width and average character length
CHARACTER_LENGTH = 4.5
LINE_WIDTH = round(ctypes.windll.user32.GetSystemMetrics(1) / CHARACTER_LENGTH)

# Colour codes
RED = '\033[31m'
BLUE = '\033[34m'
CYAN = '\033[36m'
MAGENTA = '\033[35m'
YELLOW = '\033[33m'
GREEN = '\033[32m'
# Code after string to indicate end of color use
END_COLOR = '\033[m'


# Scores
# Tic Tac Toe
player_player_2_score = 0
player_easy_computer_score = 0
player_medium_computer_score = 0
player_hard_computer_score = 0
# Minesweeper
sections_solved = 0
# Sudoku
puzzles_solved = 0

# List
scores = [player_player_2_score, player_easy_computer_score, player_medium_computer_score, player_hard_computer_score,
          sections_solved, puzzles_solved]


# Inputs
def get_input(statement, remove_spaces=True, loop=True, closed_question=False, integer=False, empty=False):
    """A template for different sorts of inputs"""

    # Set error_statement
    error_statement = None

    # Input loop
    inserting = True
    while inserting:
        # Ask and store input
        for lines in statement:
            print(YELLOW + lines.center(LINE_WIDTH) + END_COLOR)
        data = input(": ").lower()

        # Yes/No input
        if closed_question:
            data = data.lower().replace(" ", "")
            if data != "y" and data != "yes" and data != "n" and data != "no":
                error_statement = "ERROR: Please enter 'Yes(Y) or 'No(N)'."
        # Empty input
        elif data.replace(" ", "") == "":
            if not empty:
                error_statement = "ERROR: Please enter an input"
        # Integer input
        elif integer:
            try:
                data = int(data.replace(" ", ""))
            except ValueError:
                error_statement = "ERROR: Please enter an integer."

        # Display error statement if error occurred
        if error_statement is not None:
            print(GREEN + error_statement.center(LINE_WIDTH) + END_COLOR + "\n")
            # Loop for input again if loop=True
            if loop:
                error_statement = None
                continue
            else:
                break
        # Remove spaces
        else:
            if remove_spaces and type(data) == str:
                data = data.replace(" ", "")

        # Return input
        return data


# Get and confirm a name.
def ask_name():
    """Get a confirmed name from user"""

    # Line break
    print("\n")

    # Input loop
    inserting = True
    while inserting:
        name = get_input(["Please enter your name"], False).title().strip()
        confirm = get_input(["Confirmed? (Y/N)"], True, True, True)

        if confirm == "y" or confirm == "yes":
            return name


# Get difficulty
def get_level():
    """Get difficulty of a game from user"""

    inserting = True
    while inserting:
        difficulty = get_input(["Enter difficulty of puzzle:  EASY(E)  MEDIUM(M)  HARD(H)"])
        if difficulty == "e" or difficulty == "easy":
            return "easy"
        elif difficulty == "m" or difficulty == "medium":
            return "medium"
        elif difficulty == "h" or difficulty == "hard":
            return "hard"
        else:
            error_statement = "ERROR: Please enter either 'Easy', 'Medium' or 'Hard'."
            print(GREEN + error_statement.center(LINE_WIDTH) + END_COLOR + "\n")
