#!/usr/bin/python3
from pychess_ai.algos import Algo
from pychess_ai.chessai import ChessAi
from timeit import default_timer as timer
import chess

def main():
    # board_fen_string = "3k4/8/1q5p/8/8/4B3/7R/4K3 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # next_move = runminimax(board, 1, chess.WHITE, Algo.ABP)
    # print(next_move)
    # board.push(next_move)
    # print(board)

    # print("------")

    # board_fen_string = "3k4/7R/1q5p/8/8/4B3/6Q1/4K3 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # next_move = runminimax(board, 3, chess.WHITE, Algo.ABP)
    # print(next_move)
    # board.push(next_move)
    # print(board)

    # print("------")

    # board_fen_string = "1q4k1/5ppp/8/8/3BQ3/8/8/4RK2 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # next_move = runminimax(board, 3, chess.WHITE, Algo.ABP)
    # print(next_move)
    # board.push(next_move)
    # print(board)

    print("------")

    board_fen_string = "4r1k1/5ppp/4q3/5b2/8/8/5PPP/1Q4K1 b - - 0 1"
    chess_ai = ChessAi(Algo.ABP, 3, board_fen_string)
    chess_ai.print_board()
    start = timer()
    next_move = chess_ai.take_turn(chess.BLACK)
    end = timer()
    print("ABP Time : {} ABP Move : {}".format((end-start), next_move))

    print("------")

    board_fen_string = "4r1k1/5ppp/4q3/5b2/8/8/5PPP/1Q4K1 b - - 0 1"
    chess_ai = ChessAi(Algo.NO_ABP, 3, board_fen_string)
    chess_ai.print_board()
    start = timer()
    next_move = chess_ai.take_turn(chess.BLACK)
    end = timer()
    print("ABP Time : {} ABP Move : {}".format((end-start), next_move))

    # board_fen_string = "4rk2/p4ppp/1p2p3/3p4/3P4/1P2P3/P4PPP/4RK2 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # start = timer()
    # next_move = runminimax(board, 5, chess.WHITE, Algo.ABP)
    # end = timer()
    # print("ABP Time : {} ABP Move : {}".format((end-start), next_move))
    # board.push(next_move)
    # print(board)


if __name__ == '__main__':
    main()
