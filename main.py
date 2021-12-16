#!/usr/bin/python3
import chess
import typing

from enum import Enum

# Very basic evaluation function
def evaluate(board: chess.Board, num_moves: int, color_to_play: chess.Color) -> float:
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

def minimax (board: chess.Board, depth: int, num_moves: int, is_maximizing: bool, color_to_play: chess.Color) -> float:
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
            best_move = max(best_move, minimax(board, depth-1, num_moves+1, not is_maximizing, color_to_play))
            board.pop()

        else:
            board.push(move)
            best_move = min(best_move, minimax(board, depth-1, num_moves+1, not is_maximizing, color_to_play))
            board.pop()

    return best_move

# This function might be unnecessary we'll see
def runminimax(board : chess.Board, depth: int, color_to_play: chess.Color) -> str:

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
            eval = minimax(board, depth, 0, not is_maximizing, color_to_play)
            print(move, eval)
            board.pop()
            if(eval > best_eval):
                best_eval = eval
                best_move = move

    return best_move

def main():
    board_fen_string = "3k4/8/1q5p/8/8/4B3/7R/4K3 w - - 0 1"
    board = chess.Board(fen=board_fen_string)
    print(board)
    next_move = runminimax(board, 2, chess.WHITE)
    print(next_move)
    board.push(next_move)
    print(board)
    
    print("------")

    board_fen_string = "3k4/7R/1q5p/8/8/4B3/6Q1/4K3 w - - 0 1"
    board = chess.Board(fen=board_fen_string)
    print(board)
    next_move = runminimax(board, 3, chess.WHITE)
    print(next_move)
    board.push(next_move)
    print(board)

    board_fen_string = "1q4k1/5ppp/8/8/3BQ3/8/8/4RK2 w - - 0 1"
    board = chess.Board(fen=board_fen_string)
    print(board)
    next_move = runminimax(board, 3, chess.WHITE)
    print(next_move)
    board.push(next_move)
    print(board)

    # for move in board.generate_legal_moves():
    #     print(move)
    # board.push_san("e3b6")



if __name__ == '__main__':
    main()