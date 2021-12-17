from pychess_ai.algos import Algo, MiniMax, MiniMaxABP
import chess


class ChessAi:
    def __init__(
        self, algo_type: Algo, depth: int = 3, starting_fen: str = None
    ) -> None:
        if str is None:
            self._board = chess.Board()
        else:
            self._board = chess.Board(fen=starting_fen)

        if algo_type == Algo.ABP:
            self._ai = MiniMaxABP(depth)
        elif algo_type == Algo.NO_ABP:
            self._ai = MiniMax(depth)

    def update_with_move(self, move: chess.Move):
        # TODO (dan) At some point make this check legal moves, but for now we'll control that
        self._board.push(move)

    def take_turn(self, color: chess.Color) -> str:
        next_move = self.get_next_move(color)
        self._board.push(next_move)
        print(self._board)
        return next_move

    def get_next_move(self, color: chess.Color) -> str:
        return self._ai.get_next_move(self._board, color)

    def print_board(self) -> None:
        print(self._board)
