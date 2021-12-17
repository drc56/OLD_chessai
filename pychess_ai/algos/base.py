#!/usr/bin/python3
from abc import ABC, abstractmethod
from collections import deque
from enum import Enum
from pychess_ai.evaluator import Evaluator
import chess

class Algo(Enum):
    """Enum for selecting which algorithm to run
    """
    ABP = 0
    NO_ABP = 1

class BaseChessAlgo(ABC):
    def __init__(self, depth: int):
        self._depth = depth
        self._evaluator = Evaluator()

    @abstractmethod
    def get_next_move(self, board: chess.Board, color_to_play: chess.Color) -> chess.Move:
        raise NotImplementedError("Base Class doesn't have a get_next_move")

    @staticmethod
    def generate_check_capture_move_list_order(board: chess.Board) -> deque:
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
        return legal_moves
