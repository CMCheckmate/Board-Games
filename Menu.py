# Import Modules/Project files/Game files
from Settings import *
from TicTacToe import tic_tac_toe
from Sudoku import sudoku
from Minesweeper import minesweeper
import time


# Menu
# Run as MAIN
if __name__ == "__main__":
    # Get name
    username = ask_name()

    # Program loop
    playing = "y"
    while playing == "y" or playing == "yes":
        # Menu display
        # Box top
        print(("==" + "=" * 53 + "==").center(LINE_WIDTH))
        print(("||" + "=" * 53 + "||").center(LINE_WIDTH))
        # Blank lines (x1)
        print(("||" + " " * 53 + "||").center(LINE_WIDTH))
        # Header/Title
        print(("||" + BLUE +
               "                  T E X T  G A M E S                 " +
               END_COLOR + "||").center(LINE_WIDTH + len(BLUE + END_COLOR)))
        print(("||" + BLUE +
               "                          by                         " +
               END_COLOR + "||").center(LINE_WIDTH + len(BLUE + END_COLOR)))
        print(("||" + BLUE +
               "                     Ming Ray Goy                    " +
               END_COLOR + "||").center(LINE_WIDTH + len(BLUE + END_COLOR)))
        # Blank lines (x2)
        print(("||" + " " * 53 + "||").center(LINE_WIDTH))
        print(("||" + " " * 53 + "||").center(LINE_WIDTH))
        # Game Options
        print(("||" + GREEN +
               "    TicTacToe(T)     Sudoku(S)     Minesweeper(M)    " +
               END_COLOR + "||").center(LINE_WIDTH + len(GREEN + END_COLOR)))
        # Blank lines (x1)
        print(("||" + " " * 53 + "||").center(LINE_WIDTH))
        # Box bottom/cover
        print(("||" + "=" * 53 + "||").center(LINE_WIDTH))
        print(("==" + "=" * 53 + "==").center(LINE_WIDTH) + "\n")

        # Get Game choice
        game_choice = get_input(["Choose your game"], True, False)

        # Run games according to choice
        if game_choice == "tictactoe" or game_choice == "t":
            # TicTacToe
            tic_tac_toe(username)
        elif game_choice == "sudoku" or game_choice == "s":
            # Sudoku
            sudoku(username)
        elif game_choice == "minesweeper" or game_choice == "m":
            # Minesweeper
            minesweeper(username)
        # Error statement (Incorrect choice)
        elif game_choice is not None:
            error_statement = \
                "ERROR: Please enter a game choice from the options below."
            print(GREEN + error_statement.center(LINE_WIDTH) +
                  END_COLOR + "\n")
            time.sleep(1)
            continue
        # Empty input
        else:
            time.sleep(1)
            continue

        # Delay
        time.sleep(1)

        # Get choice to play again
        playing = get_input(["Choose another game? (Y/N)"], True, True, True)

    # Delay
    time.sleep(1)

    # Quit
    print(MAGENTA + "\n" + ("Goodbye " + username + "!").center(LINE_WIDTH) +
          END_COLOR)
