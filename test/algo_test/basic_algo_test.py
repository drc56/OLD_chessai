from pychess_ai.algos import MiniMaxABP, MiniMax
import chess

def test_construction_abp():
    algo = MiniMaxABP(3)
    assert isinstance(algo, MiniMaxABP)

def test_construction_minimax():
    algo = MiniMax(3)
    assert isinstance(algo, MiniMax)
