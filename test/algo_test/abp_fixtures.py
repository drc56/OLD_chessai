from attr import dataclass
import pytest
import chess
from pychess_ai.algos import MiniMaxABP


@dataclass
class ABPTestStructure:
    algo: MiniMaxABP
    board: chess.Board
    color_to_play: chess.Color


@pytest.fixture
def ABP_setup():
    def _make_test_setup(fen: str, depth: int, logging):
        test_setup = ABPTestStructure(None, None, None)
        test_setup.board = chess.Board(fen=fen)
        test_setup.algo = MiniMaxABP(depth, log_level=logging)
        test_setup.color_to_play = test_setup.board.turn
        return test_setup

    return _make_test_setup
