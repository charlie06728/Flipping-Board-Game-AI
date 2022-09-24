"""
An AI agent for land bidding process.
"""
import random
import sys
import time

# You can use the functions in utilities to write your AI
from utilities import find_lines, get_possible_moves, get_score, play_move

cached_states = {}


def eprint(*args,
           **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    own = color - 1
    op = 3 - color - 1
    return get_score(board)[own] - get_score(board)[op]


# Better heuristic value of board
def compute_heuristic(board, color):  # not implemented, optional
    # IMPLEMENT
    possible_moves = get_possible_moves(board, color)
    if possible_moves == []:
        return compute_utility(board, color)

    flip_num = []
    for move in possible_moves:
        num = 0
        lines = find_lines(board, move[0], move[1], color)
        for line in lines:
            num += len(line)
        flip_num.append(num)

    possible_moves = get_possible_moves(board, 3 - color)
    op_flip_num = []
    for move in possible_moves:
        num = 0
        lines = find_lines(board, move[0], move[1], 3 - color)
        for line in lines:
            num += len(line)
        op_flip_num.append(num)

    max_fnum = max(flip_num)
    op_max_fnum = max(op_flip_num)
    return max_fnum - op_max_fnum + compute_utility(board, color)


############ MINIMAX ###############################
def mm_min_node(board, color, limit, caching=0):
    # IMPLEMENT (and replace the line below)
    possible_moves = get_possible_moves(board, color)
    if possible_moves == []:
        return ((0, 0), -1 * compute_utility(board, color))
    elif limit == 0:
        return ((0, 0), -1 * compute_heuristic(board, color))

    move_scores = []
    for move in possible_moves:
        curr_board = play_move(board, color, move[0], move[1])
        if caching == 1:
            cache = _check_cache(board, color)
            if cache is None:
                score = mm_max_node(curr_board, 3 - color, limit - 1, caching)[1]
                cached_states[(curr_board, color)] = score
            else:
                score = cached_states[(curr_board, color)]
        else:
            score = mm_max_node(curr_board, 3 - color, limit - 1, caching)[1]
        move_scores.append(score)

    min_score_index = move_scores.index(min(move_scores))
    return (possible_moves[min_score_index], move_scores[min_score_index])


def mm_max_node(board, color, limit, caching=0):
    # IMPLEMENT (and replace the line below)
    possible_moves = get_possible_moves(board, color)

    if possible_moves == [] or limit == 0:
        return ((0, 0), compute_utility(board, color))
    elif limit == 0:
        return ((0, 0), compute_utility(board, color))

    move_scores = []
    for move in possible_moves:
        curr_board = play_move(board, color, move[0], move[1])
        if caching == 1:
            cache = _check_cache(curr_board, color)
            if cache is None:
                score = mm_min_node(curr_board, 3 - color, limit - 1, caching)[1]
                cached_states[(curr_board, color)] = score
            else:
                score = cached_states[(curr_board, color)]
        else:
            score = mm_min_node(curr_board, 3 - color, limit - 1, caching)[1]
        move_scores.append(score)

    max_score_index = move_scores.index(max(move_scores))
    return (possible_moves[max_score_index], move_scores[max_score_index])


def claim_mm(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function: If limit is a positive integer,
    your code should enfoce a depth limit that is equal to the value of the parameter. Search
    only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal
    return a heuristic value (see compute_utility) If caching is ON (i.e. 1), use state caching
    to reduce the number of state evaluations. If caching is OFF (i.e. 0), do NOT use state
    caching to reduce the number of state evaluations.
    """
    return mm_max_node(board, color, limit, caching)[0]


############ ALPHA-BETA PRUNING #####################
def ab_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    b_move = None
    possible_moves = get_possible_moves(board, color)

    # If the ordering is 1, use BFS
    if ordering == 1:
        order_stack = []
        for move in possible_moves:
            curr_board = play_move(board, color, move[0], move[1])

            if get_possible_moves(curr_board, 3 - color) == [] or limit == 0:  # A terminal state is reached
                # utility = get_score(curr_board)[0] - get_score(curr_board)[1]
                utility = compute_utility(curr_board, 3 - color)
                if utility < beta:
                    beta = utility
                    b_move = move
                    if alpha >= beta:
                        return (b_move, beta)
            else:
                order_stack.append((move, curr_board))
        for move, item in order_stack:
            utility = ab_max_node(item, 3 - color, alpha, beta, limit, caching, ordering)[1]
            if utility < beta:
                beta = utility
                b_move = move
                if alpha >= beta:
                    break
        return (b_move, beta)


    if possible_moves == []:
        return (None, -1 * compute_utility(board, color))
    elif limit == 0:
        return (None, -1 * compute_utility(board, color))

    for move in possible_moves:
        curr_board = play_move(board, color, move[0], move[1])
        if caching == 1:
            cache = _check_cache(curr_board, color)
            if cache is None:
                utility = ab_max_node(curr_board, 3 - color, alpha, beta, limit - 1, caching,
                                      ordering)[1]
                cached_states[(curr_board, color)] = utility
            else:
                utility = cache
        else:
            utility = ab_max_node(curr_board, 3 - color, alpha, beta, limit - 1, caching, ordering)[
                1]

        if utility < beta:
            beta = utility
            b_move = move
            if alpha >= beta:
                break

    return (b_move, beta)


def ab_max_node(board, color, alpha, beta, limit, caching=0, ordering=0) -> tuple:
    b_move = None
    possible_moves = get_possible_moves(board, color)

    # If the ordering is 1, use BFS
    if ordering == 1:
        order_stack = []
        for move in possible_moves:
            curr_board = play_move(board, color, move[0], move[1])

            if get_possible_moves(curr_board,
                                  3 - color) == [] or limit == 0:  # A terminal state is reached
                # utility = get_score(curr_board)[0] - get_score(curr_board)[1]
                utility = -1 * compute_utility(curr_board, 3 - color)
                if utility > alpha:
                    alpha = utility
                    b_move = move
                    if alpha >= beta:
                        return (b_move, alpha)
            else:
                order_stack.append((move, curr_board))
        for move, item in order_stack:
            utility = ab_min_node(item, 3 - color, alpha, beta, limit, caching, ordering)[1]
            if utility > alpha:
                alpha = utility
                b_move = move
                if alpha >= beta:
                    break
        return (b_move, alpha)

    if possible_moves == []:
        return (None, compute_utility(board, color))
    elif limit == 0:
        return (None, compute_utility(board, color))

    for move in possible_moves:
        curr_board = play_move(board, color, move[0], move[1])
        if caching == 1:
            cache = _check_cache(curr_board, color)
            if cache is None:
                utility = ab_min_node(curr_board, 3 - color, alpha, beta, limit - 1, caching,
                                      ordering)[1]
                cached_states[(curr_board, color)] = utility
            else:
                utility = cache
        else:
            utility = ab_min_node(curr_board, 3 - color, alpha, beta, limit - 1, caching, ordering)[
                1]

        if utility > alpha:
            alpha = utility
            b_move = move
            if alpha >= beta:
                break

    return (b_move, alpha)


def claim_ab(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function: If limit is a positive integer,
    your code should enfoce a depth limit that is equal to the value of the parameter. Search
    only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal
    return a heuristic value (see compute_utility) If caching is ON (i.e. 1), use state caching
    to reduce the number of state evaluations. If caching is OFF (i.e. 0), do NOT use state
    caching to reduce the number of state evaluations. If ordering is ON (i.e. 1), use node
    ordering to expedite pruning and reduce the number of state evaluations. If ordering is OFF (
    i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state
    evaluations.
    """
    minimum_score = len(board) ** 2 * -1
    maximum_score = len(board) ** 2 + 1

    alpha = minimum_score
    beta = maximum_score
    move = ab_max_node(board, color, alpha, beta, limit, caching, ordering)[0]
    return move


def _check_cache(board, color):
    """Check is the same state has been reached before
    """
    if (board, color) not in cached_states:
        return None
    else:
        return cached_states[(board, color)]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Bidding AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if (minimax == 1):
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if (caching == 1):
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if (ordering == 1):
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1):  # run this if the minimax flag is given
                movei, movej = claim_mm(board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = claim_ab(board, color, limit, caching, ordering)


            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
