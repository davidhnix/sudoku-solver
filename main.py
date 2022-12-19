import datetime

TEST_BOARD = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
              [6, 0, 0, 0, 7, 5, 0, 0, 9],
              [0, 0, 0, 6, 0, 1, 0, 7, 8],
              [0, 0, 7, 0, 4, 0, 2, 6, 0],
              [0, 0, 1, 0, 5, 0, 9, 3, 0],
              [9, 0, 4, 0, 6, 0, 0, 0, 5],
              [0, 7, 0, 3, 0, 0, 0, 1, 2],
              [1, 2, 0, 0, 0, 7, 4, 0, 0],
              [0, 4, 9, 2, 0, 6, 0, 0, 7]]


def find_blank_locations(board):
    blank_locations = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                blank_locations.append((i, j))

    return blank_locations


def grid_is_correct(grid_marker, board):
    grid_values = []
    for i in range(grid_marker[0], grid_marker[0] + 3):
        for j in range(grid_marker[1], grid_marker[1] + 3):
            current_value = board[i][j]
            if current_value == 0:
                continue  # this is blank and we don't care about it

            if current_value in grid_values:
                return False  # we've got two of the same values in the grid

            grid_values.append(current_value)

    return True


def grids_are_correct(board, guess_location):
    grid_markers = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

    target_marker = ()
    for grid_marker in grid_markers:
        if grid_marker[0] <= guess_location[0] <= grid_marker[0] + 2 and grid_marker[1] <= guess_location[1] <= grid_marker[1] + 2:
            target_marker = grid_marker  # our guess location is within this grid marked by this grid_marker

    if target_marker == ():
        raise Exception("Could not find which grid to check.....fix the bad code")

    return grid_is_correct(target_marker, board)  # only check the grid we're guessing in


def rows_are_correct(board, guess_location):
    target_row = board[guess_location[0]]  # only check the row we're guessing in

    row_values = []
    for i in range(len(target_row)):
        current_value = target_row[i]
        if current_value == 0:
            continue  # we dont care about blanks

        if current_value in row_values:
            return False  # we already have this guess in this row

        row_values.append(current_value)

    return True


def columns_are_correct(board, guess_location):

    column_values = []
    for row_index in range(len(board)):
        current_value = board[row_index][guess_location[1]]  # only check the column we're guessing in
        if current_value == 0:
            continue  # we dont care about blanks when checking column values

        if current_value in column_values:
            return False  # we found a duplicate in this column

        column_values.append(current_value)

    return True


def board_is_correct(board, guess_location):
    if not grids_are_correct(board, guess_location):
        return False
    if not rows_are_correct(board, guess_location):
        return False
    if not columns_are_correct(board, guess_location):
        return False

    return True


def board_is_complete(working_board):
    for row_index in range(len(working_board)):
        for column_index in range(len(working_board[0])):
            if working_board[row_index][column_index] == 0:  # this indicates a non-guessed space
                return False

    return True


def solve_puzzle(initial_board):
    print_board(initial_board)

    start_time = datetime.datetime.now()

    final_board = solve_with_backtracking(initial_board)

    end_time = datetime.datetime.now()
    print(f"completed solution in: {float((end_time - start_time).total_seconds() * 1000)}ms")

    print("YAY! Board complete!")
    print("Solution:")
    print_board(final_board)


def solve_with_backtracking(initial_board):
    # create a list of the spaces we need to fill in
    blank_locations = find_blank_locations(initial_board)
    # iterate over the list of blank locations
    guess_counter = 0
    board_complete = False
    board_correct = False
    working_board = initial_board
    while not board_complete or not board_correct:
        guess_location = blank_locations[guess_counter]
        current_guess = working_board[guess_location[0]][guess_location[1]]
        if current_guess == 9:
            # we're not able to make more guesses here. need to backtrack
            guess_counter -= 1
            working_board[guess_location[0]][
                guess_location[1]] = 0  # wipe out anything we've guessed if we're backtracking
            continue

        new_guess = current_guess + 1  # try to the next highest number
        working_board[guess_location[0]][guess_location[1]] = new_guess

        # check board to see if valid
        if board_is_correct(working_board, guess_location):
            board_correct = True
        else:
            continue  # no need to do anything else if not correct as is

        # check board to see if complete
        if board_is_complete(working_board):
            board_complete = True
        else:
            guess_counter += 1  # set up for the next guess
            print("moving foward.....")
            print_board(working_board)

    return working_board


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print(" -  -  -   -  -  -   -  -  - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|", end="")

            print(f" {board[i][j] if board[i][j] != 0 else ' '} ", end="")

        print("")


if __name__ == '__main__':
    solve_puzzle(TEST_BOARD)


