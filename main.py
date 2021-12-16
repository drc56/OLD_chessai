#!/usr/bin/python3
from collections import deque, OrderedDict
from enum import Enum
from timeit import default_timer as timer
import chess

class Algo(Enum):
    """Enum for selecting which algorithm to run
    """
    ABP = 0
    NO_ABP = 1

def evaluate(board: chess.Board, num_moves: int, color_to_play: chess.Color) -> float:
    """Chess position evaluation function

    Args:
        board (chess.Board): A python-chess board
        num_moves (int): How many moves deep are we int the evaluation
        color_to_play (chess.Color): What color are we evaluating for at the root

    Returns:
        float: The evaluation
    """
    evaluation = 0.0
    if board.is_checkmate():
        return 1000.0 - num_moves

    material_value = 0.0
    for square, piece in board.piece_map().items():
        piece_value = 0.0
        if piece.piece_type == chess.PAWN:
            piece_value = 1.0
        elif piece.piece_type == chess.KNIGHT:
            piece_value = 3.0
        elif piece.piece_type == chess.BISHOP:
            piece_value = 3.0
        elif piece.piece_type == chess.ROOK:
            piece_value = 5.0
        elif piece.piece_type == chess.QUEEN:
            piece_value = 9.0
        if color_to_play is piece.color:
            material_value += piece_value
        else:
            material_value -= piece_value

    evaluation += material_value

    return evaluation


def minimax_abp(board: chess.Board, depth: int, num_moves: int, is_maximizing: bool, alpha: int, beta: int, color_to_play: chess.Color) -> float:
    """Minimax with alpha beta pruning

    Args:
        board (chess.Board): python chess board of current position.
        depth (int): how many levels deeper to go.
        num_moves (int): number of moves into evaluation we are.
        is_maximizing (bool): indication of if maximising or minimizing step.
        alpha (int): the value for alpha.
        beta (int): the value for beta.
        color_to_play (chess.Color): what color is playing at the root.

    Returns:
        float: evaluation.
    """
    # Base case for mini max, which should trigger on checkmates as well
    # print("Alpha: {} Beta: {}".format(alpha, beta))

    if(depth == 0 or board.is_checkmate()):
        return evaluate(board, num_moves, color_to_play)

    # Set the eval to either very large negative of very large positive
    if(is_maximizing):
        best_move = -9999
    else:
        best_move = 9999

    # Let's make a move deque to sort it so checks and captures are front of the list
    # Also going to make a hokey dictionary for storing capture moves...since there's a generate function
    # Honestly not sure if that generate function is quick...
    legal_moves = deque()
    capture_moves = set()

    # Generate a list of all legal moves to play in this position
    legal_moves_list = board.generate_legal_moves()
    capture_move_list = board.generate_legal_captures()

    for move in capture_move_list:
        legal_moves.append(move)
        capture_moves.add(move)

    for move in legal_moves_list:
        # Going to do a quick check if the move creates check
        board.push(move)
        if(board.is_check()):
            legal_moves.appendleft(move)
        else:
            if move not in capture_moves:
                legal_moves.append(move)
        board.pop()

    # let's step through each legal move
    while legal_moves:
        move = legal_moves.popleft()
        if(is_maximizing):
            board.push(move)
            best_move = max(best_move, minimax_abp(
                board, depth-1, num_moves+1, not is_maximizing, alpha, beta, color_to_play))
            board.pop()
            alpha = max(alpha, best_move)
            if(beta <= alpha):
                break

        else:
            board.push(move)
            best_move = min(best_move, minimax_abp(
                board, depth-1, num_moves+1, not is_maximizing,  alpha, beta,  color_to_play))
            board.pop()
            beta = min(beta, best_move)
            if(beta <= alpha):
                break

    return best_move


def minimax(board: chess.Board, depth: int, num_moves: int, is_maximizing: bool, color_to_play: chess.Color) -> float:
    """ Minimax evaluation algorithm.

    Args:
        board (chess.Board): python chess board of current position.
        depth (int): how many levels deeper to go.
        num_moves (int): number of moves into evaluation we are.
        is_maximizing (bool): indication of if maximising or minimizing step.
        color_to_play (chess.Color): what color is playing at the root.

    Returns:
        float: evaluation.
    """
    # Base case for mini max, which should trigger on checkmates as well
    if(depth == 0 or board.is_checkmate()):
        return evaluate(board, num_moves, color_to_play)

    # Generate a list of all legal moves to play in this position
    legal_moves = board.generate_legal_moves()

    # Set the eval to either very large negative of very large positive
    if(is_maximizing):
        best_move = -9999
    else:
        best_move = 9999

    # let's step through each legal move
    for move in legal_moves:
        if(is_maximizing):
            board.push(move)
            best_move = max(best_move, minimax(
                board, depth-1, num_moves+1, not is_maximizing, color_to_play))
            board.pop()

        else:
            board.push(move)
            best_move = min(best_move, minimax(
                board, depth-1, num_moves+1, not is_maximizing, color_to_play))
            board.pop()

    return best_move

# This function might be unnecessary we'll see


def runminimax(board: chess.Board, depth: int, color_to_play: chess.Color, algo_type: Algo) -> str:
    """Root for minimax

    Args:
        board (chess.Board): python chess board of current position.
        depth (int): how many levels deeper to go.
        color_to_play (chess.Color): what color is playing at the root.
        algo_type (Algo): inidication on what algorithm to use.

    Returns:
        str: move to play.
    """

    best_move = ""
    best_eval = -9999

    # Generate a list of all legal moves
    legal_moves = board.generate_legal_moves()

    # We also start as the maximizing player as we are making the move
    is_maximizing = True

    # let's step through each legal move
    for move in legal_moves:
        if(is_maximizing):
            board.push(move)
            if algo_type is Algo.ABP:
                eval = minimax_abp(
                    board, depth, 0, not is_maximizing, -9999, 9999, color_to_play)
            elif algo_type is Algo.NO_ABP:
                eval = minimax(board, depth, 0,
                               not is_maximizing, color_to_play)
            board.pop()
            if(eval > best_eval):
                best_eval = eval
                best_move = move

    return best_move


def main():
    board_fen_string = "3k4/8/1q5p/8/8/4B3/7R/4K3 w - - 0 1"
    board = chess.Board(fen=board_fen_string)
    print(board)

    next_move = runminimax(board, 2, chess.WHITE, Algo.ABP)
    print(next_move)
    board.push(next_move)
    print(board)

    print("------")

    board_fen_string = "3k4/7R/1q5p/8/8/4B3/6Q1/4K3 w - - 0 1"
    board = chess.Board(fen=board_fen_string)
    print(board)
    next_move = runminimax(board, 3, chess.WHITE, Algo.ABP)
    print(next_move)
    board.push(next_move)
    print(board)

    print("------")

    board_fen_string = "1q4k1/5ppp/8/8/3BQ3/8/8/4RK2 w - - 0 1"
    board = chess.Board(fen=board_fen_string)
    print(board)
    next_move = runminimax(board, 3, chess.WHITE, Algo.ABP)
    print(next_move)
    board.push(next_move)
    print(board)

    print("------")

    board_fen_string = "4r1k1/5ppp/4q3/5b2/8/8/5PPP/1Q4K1 b - - 0 1"
    board = chess.Board(fen=board_fen_string)
    print(board)
    start = timer()
    next_move = runminimax(board, 3, chess.BLACK, Algo.ABP)
    end = timer()
    print("ABP Time : {} ABP Move : {}".format((end-start), next_move))
    board.push(next_move)
    print(board)


if __name__ == '__main__':
    main()
