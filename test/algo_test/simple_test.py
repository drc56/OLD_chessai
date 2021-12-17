from pychess_ai.chessai import ChessAi
from pychess_ai.algos import Algo

def test_construction():
    chess_ai = ChessAi(Algo.ABP)
    assert(True)
