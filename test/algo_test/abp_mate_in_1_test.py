from pychess_ai.algos import MiniMaxABP
import chess

TESTING_DEPTH = 1


def board_setup(fen: str) -> chess.Board:
    return chess.Board(fen=fen)


def test_position_one():

    # Setup the Board
    position_fen = "1Q6/p7/q1p3p1/3p4/2kPpP2/4P1P1/P2B2K1/3r4 w - - 4 34"
    board = board_setup(fen=position_fen)

    # Create the Algo to test
    algo = MiniMaxABP(depth=TESTING_DEPTH)

    # TODO(dan) make a utility to extract color to play from a FEN
    next_move = algo.get_next_move(board, chess.WHITE)

    assert board.san(next_move) == "Qb3#"
