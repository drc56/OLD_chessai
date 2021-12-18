from pychess_ai.algos import MiniMaxABP
import chess
import pytest

TESTING_DEPTH = 1


def board_setup(fen: str) -> chess.Board:
    return chess.Board(fen=fen)


@pytest.mark.skip
@pytest.mark.xfail
def test_position_one():

    # Setup the Board
    position_fen = "5bk1/6p1/p1qr1pQP/1p2r3/1P6/P1NR4/5PP1/6K1 w - - 0 38"
    board = board_setup(fen=position_fen)

    # Create the Algo to test
    algo = MiniMaxABP(depth=TESTING_DEPTH)

    # TODO(dan) make a utility to extract color to play from a FEN
    next_move = algo.get_next_move(board, chess.WHITE)
    assert board.san(next_move) == "h7+"

    # Play the move this is a two move tactic
    board.push(next_move)

    # The King will move to the corner here
    board.push_san("Kh8")
    next_move = algo.get_next_move(board, chess.WHITE)

    assert board.san(next_move) == "Qf7"
