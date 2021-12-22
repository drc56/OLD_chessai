from pychess_ai.algos import Algo, MiniMax, MiniMaxABP
import chess
import logging

DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class ChessAi:
    def __init__(
        self,
        algo_type: Algo,
        depth: int = 3,
        color_to_play: chess.Color = chess.WHITE,
        starting_fen: str = DEFAULT_FEN,
        logging_level=logging.INFO,
    ) -> None:

        self._board = chess.Board(fen=starting_fen)
        self._color = color_to_play
        if algo_type == Algo.ABP:
            self._ai = MiniMaxABP(depth, log_level=logging_level)
        elif algo_type == Algo.NO_ABP:
            self._ai = MiniMax(depth)

    def update_with_move(self, move: str) -> bool:
        # TODO (dan) At some point make this check legal moves, but for now we'll control that
        try:
            if self._board.is_legal(self._board.parse_san(move)):
                self._board.push_san(move)
                return True
        except ValueError:
            return False
        return False

    def take_turn(self) -> str:
        next_move = self._board.san(self.get_next_move(self._color))
        self._board.push_san(next_move)
        print(self._board)
        return next_move

    def get_next_move(self, color: chess.Color) -> chess.Move:
        return self._ai.get_next_move(self._board, color)

    def print_board(self) -> None:
        print(self._board)

    def is_game_over(self) -> bool:
        return self._board.is_checkmate()
