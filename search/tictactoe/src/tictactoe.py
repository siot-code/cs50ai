"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    summary: count X's and O's to determine whose turn it is
    for each X +1 and for each O -1. if result +1 it is O turn if 0 it is X 
    """
    count=0
    for row in board:
        for cell in row:
            count += 1 if cell == "X" else -1 if cell == "O" else 0
    if count == 1:
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_actions.add((i,j))
    return possible_actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    TODO verify that i and j are acceptable values
    """
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)

    return board_copy


def winner(board):
    symbol_to_value = {X: 1, O: -1, EMPTY: 0}
    num_board = [[symbol_to_value[cell] for cell in row] for row in board]

    row_sums = [sum(row) for row in num_board]
    col_sums = [sum(col) for col in zip(*num_board)]
    diag_sums = [
        sum(num_board[i][i] for i in range(len(num_board))),
        sum(num_board[i][len(num_board) - 1 - i] for i in range(len(num_board)))
    ]

    if 3 in row_sums or 3 in col_sums or 3 in diag_sums:
        return X
    elif -3 in row_sums or -3 in col_sums or -3 in diag_sums:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    # Game is over if there are no EMPTY cells left
    return not any(EMPTY in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): #is game finished
        return None

    current_player = player(board)

    best_move = None
    
    if current_player == X:
        best_score = -float('inf')
        for action in actions(board):
            score = min_value(result(board,action))
            if(score > best_score):
                best_score = score
                best_move = action
    else:
        best_score = float('inf')
        for action in actions(board):
            score = max_value(result(board,action))
            if(score < best_score):
                best_score = score
                best_move = action
    return best_move




def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board,action)))
    return v


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -float('inf')
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    return v