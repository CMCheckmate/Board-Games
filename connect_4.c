#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char EMPTY_SPACE = ' ';
const char PLAYER_1 = 'O';
const char PLAYER_2 = 'X';
const int DRAW = -1;
const int GRID_COLUMNS = 7;
const int GRID_ROWS = 6;
const int NUM_CONNECT = 4;

void show_board(char** grid) {
    char grid_char;
    
    printf("\n");
    for (int i = GRID_ROWS - 1; i >= 0; i--) {
        printf("|");
        for (int j = 0; j < GRID_COLUMNS; j++) {
            grid_char = grid[i][j];
            printf("|%c|", grid_char);
        }
        printf("|\n");
    }
}

char** setup_board() {
    char** grid = malloc(GRID_ROWS * sizeof(char*));

    for (int i = 0; i < GRID_ROWS; i++) {
        grid[i] = malloc(GRID_COLUMNS * sizeof(char));
        for (int j = 0; j < GRID_COLUMNS; j++) {
            grid[i][j] = EMPTY_SPACE;
        }
    }

    return grid;
}

int check_win(char** grid) {
    int diagonal_up_connect;
    int diagonal_down_connect;
    int vertical_connect;
    int horizontal_connect;
    int draw = 1;
    int game_state = 0;

    for (int i = 0; i < GRID_ROWS; i++) {
        for (int j = 0; j < GRID_COLUMNS; j++) {
            if (grid[i][j] == EMPTY_SPACE && draw) {
                draw = 0;
            } else if (grid[i][j] != EMPTY_SPACE && !game_state) {
                if (grid[i][j] == PLAYER_1) {
                    game_state = 1;
                } else {
                    game_state = 2;
                }

                diagonal_up_connect = 1;
                diagonal_down_connect = 1;
                vertical_connect = 1;
                horizontal_connect = 1;

                for (int connect = 1; connect < NUM_CONNECT; connect++) {
                    if (i <= GRID_ROWS - NUM_CONNECT) {
                        if (grid[i][j] == grid[i + connect][j]) {
                            vertical_connect++;
                        }
                    }
                    if (j <= GRID_COLUMNS - NUM_CONNECT) {
                        if (grid[i][j] == grid[i][j + connect]) {
                            horizontal_connect++;
                        }
                        if (i <= GRID_ROWS - NUM_CONNECT) {
                            if (grid[i][j] == grid[i + connect][j + connect]) {
                                diagonal_up_connect++;
                            }
                        }
                        if (i >= NUM_CONNECT - 1) {
                            if (grid[i][j] == grid[i - connect][j + connect]) {
                                diagonal_down_connect++;
                            }
                        }
                    }
                }

                if (diagonal_up_connect < NUM_CONNECT && diagonal_down_connect < NUM_CONNECT && 
                    vertical_connect < NUM_CONNECT && horizontal_connect < NUM_CONNECT) {
                    game_state = 0;
                }
            }
        }
    }

    if (game_state == 0 && draw) {
        game_state = DRAW;
    }

    return game_state;
}

int* convert_move(int move, char** grid) {
    int* coordinate = malloc(2 * sizeof(int));
    int row = 0;
    int set = 0;

    for (int i = 0; i < GRID_ROWS; i++) {
        if (grid[i][move] == EMPTY_SPACE && !set) {
            row = i;
            set = 1;
        }
    }

    if (set) {
        coordinate[0] = row;
    } else {
        coordinate[0] = GRID_ROWS;
    }
    coordinate[1] = move;

    return coordinate;
}

int* get_move(char** grid) {
    #define INPUT_LENGTH 1

    char input[INPUT_LENGTH + 2];
    long move_converted;
    int* coordinate;
    int buffer;
    int valid = 0;

    while (!valid) {
        input[0] = '\0';
        printf("\nEnter your move (e.g. '1' refers to the first column): ");
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = '\0';
        if (strlen(input) > INPUT_LENGTH) {
            while ((buffer = getchar()) != '\n' && buffer != EOF) {}
        }

        move_converted = (int)strtol(input, NULL, 10);
        if (0 < move_converted && move_converted <= GRID_COLUMNS) {
            coordinate = convert_move(move_converted - 1, grid);
            if (coordinate[0] < GRID_ROWS) {
                valid = 1;
            } else {
                printf("That column is full. Please choose another column.\n");
            }
        } else {
            printf("Plese enter a valid move in the format shown (e.g. '5' for column 5).\n");
        }
    }

    return coordinate;
}

int main() {
    char** main_grid = setup_board();
    show_board(main_grid);

    char restart[3];
    int *move_coordinate;
    int game_turn = 1;
    int game_over = 0;

    while (!game_over) {
        printf("\n- PLAYER %d's turn -\n", game_turn);
        move_coordinate = get_move(main_grid);

        if (game_turn == 1) {
            main_grid[move_coordinate[0]][move_coordinate[1]] = PLAYER_1;
            game_turn = 2;
        } else {
            main_grid[move_coordinate[0]][move_coordinate[1]] = PLAYER_2;
            game_turn = 1;
        }
        free(move_coordinate);

        show_board(main_grid);

        game_over = check_win(main_grid);
        if (game_over) {
            printf("\n- GAME OVER -\n");
            if (game_over == DRAW) {
                printf("\nDRAW!\n");
            } else {
                printf("\nPLAYER %d WINS!\n", game_over);
            }

            restart[0] = '\0';
            printf("\nRestart? (Press anything to continue, 'Enter' to exit): ");
            fgets(restart, sizeof(restart), stdin);

            if (strlen(restart) > 1) {
                game_over = 0;
                game_turn = 1;
                free(main_grid);
                main_grid = setup_board();
                show_board(main_grid);
            }
        }
    }
}
