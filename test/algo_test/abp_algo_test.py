import pytest
from main import LOGGING_LEVEL
from pychess_ai.algos import MiniMaxABP
from abp_fixtures import ABP_setup
import chess
import logging

TESTING_DEPTH = 3
LOGGING_LEVEL = logging.INFO
M1_TEST_CASES = [
    ("1Q6/p7/q1p3p1/3p4/2kPpP2/4P1P1/P2B2K1/3r4 w - - 4 34", ["Qb3#"], [None]),
    ("r7/ppQ5/k7/3q1N2/3B4/N7/P3rnPP/1KR5 b - - 0 27", ["Qxa2#"], [None]),
    ("1rq2k2/1bNp1p1p/pb1Pp1p1/1p6/8/PnQ5/2P2PPP/1R3RK1 w - - 0 26", ["Qh8#"], [None]),
    ("r4b1r/pp1nk2p/3p1qp1/1Bppn3/8/7Q/PPP2PPP/R1B1R1K1 w - - 0 17", ["Qxd7#"], [None]),
    ("5k2/7R/2p2KP1/p1p2p2/5P2/1P4q1/P2p4/8 w - - 0 45", ["Rh8#"], [None]),
]

HANG_TEST_CASES = [
    (
        "2Q5/1p1r2kp/p4pq1/6p1/2P5/1PB5/P4PPK/4r3 w - - 0 42",
        ["Qxd7+", "Qxf7+", "Bxe1"],
        ["Qf7", "Kxf7", None],
    )
]


def run_test(test_setup, sol_moves, puz_moves):
    for sol, puz in zip(sol_moves, puz_moves):
        next_move = test_setup.algo.get_next_move(
            test_setup.board, test_setup.color_to_play
        )

        assert test_setup.board.san(next_move) == sol

        if puz:
            test_setup.board.push(next_move)
            test_setup.board.push_san(puz)


@pytest.mark.parametrize(
    "fen, depth, logging, sol, moves",
    [
        pytest.param(
            M1_TEST_CASES[0][0],
            TESTING_DEPTH,
            LOGGING_LEVEL,
            M1_TEST_CASES[0][1],
            M1_TEST_CASES[0][2],
        ),
        pytest.param(
            M1_TEST_CASES[1][0],
            TESTING_DEPTH,
            LOGGING_LEVEL,
            M1_TEST_CASES[1][1],
            M1_TEST_CASES[1][2],
        ),
        pytest.param(
            M1_TEST_CASES[2][0],
            TESTING_DEPTH,
            LOGGING_LEVEL,
            M1_TEST_CASES[2][1],
            M1_TEST_CASES[2][2],
        ),
        pytest.param(
            M1_TEST_CASES[3][0],
            TESTING_DEPTH,
            LOGGING_LEVEL,
            M1_TEST_CASES[3][1],
            M1_TEST_CASES[3][2],
        ),
        pytest.param(
            M1_TEST_CASES[4][0],
            TESTING_DEPTH,
            LOGGING_LEVEL,
            M1_TEST_CASES[4][1],
            M1_TEST_CASES[4][2],
        ),
    ],
)
def test_mate_in_one(ABP_setup, fen, depth, logging, sol, moves):
    test_setup = ABP_setup(fen, depth, logging)
    run_test(test_setup, sol, moves)


@pytest.mark.parametrize(
    "fen, depth, logging, sol, moves",
    [
        pytest.param(
            HANG_TEST_CASES[0][0],
            TESTING_DEPTH,
            LOGGING_LEVEL,
            HANG_TEST_CASES[0][1],
            HANG_TEST_CASES[0][2],
        ),
    ],
)
def test_hanging_pieces(ABP_setup, fen, depth, logging, sol, moves):
    test_setup = ABP_setup(fen, depth, logging)
    run_test(test_setup, sol, moves)
