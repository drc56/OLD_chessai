from collections import deque
from dataclasses import dataclass
import chess

# fmt: off
PAWN_EVAL_DICT = {
    chess.WHITE :
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0,
        1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25,
        1.0, 1.0, 1.0, 2.5, 2.5, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.5, 2.5, 2.5, 1.5, 1.0, 1.0,
        2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0,
        5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    chess.BLACK :
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
        2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0,
        1.0, 1.0, 1.5, 2.5, 2.5, 1.5, 1.0, 1.0,
        1.0, 1.0, 1.5, 2.5, 2.5, 1.5, 1.0, 1.0,
        1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25,
        1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
}

ROOK_EVAL_DICT = {
    chess.WHITE :
        [1.0, 1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.0,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    chess.BLACK :
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75,
        1.0, 1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.0],
}

QUEEN_EVAL_DICT = {
    chess.WHITE :
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    chess.BLACK :
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,
        1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
}
# fmt: on


@dataclass
class EvalReturnType:
    move: chess.Move
    eval: float
    line: deque


class Evaluator:
    def __init__(self):
        self._position_table = dict()
        pass

    def evaluate(
        self, board: chess.Board, num_moves: int, color_to_play: chess.Color
    ) -> EvalReturnType:
        """Chess position evaluation function

        Args:
            board (chess.Board): A python-chess board
            num_moves (int): How many moves deep are we int the evaluation
            color_to_play (chess.Color): What color are we evaluating for at the root

        Returns:
            float: The evaluation
        """
        # Build the line we evaluated
        line = board.move_stack[len(board.move_stack) - (num_moves + 1) :]
        # Gonna use the FEN without the turn
        epd_key = board.epd()
        if epd_key in self._position_table:
            return EvalReturnType(
                move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
                eval=self._position_table[epd_key],
                line=line,
            )

        evaluation = 0.0
        if board.is_checkmate():
            if board.outcome() == color_to_play:
                return EvalReturnType(
                    move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
                    eval=10000.0 - num_moves,
                    line=line,
                )
            else:
                return EvalReturnType(
                    move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
                    eval=(10000.0 - num_moves) * -1.0,
                    line=line,
                )

        material_value = 0.0
        for square, piece in board.piece_map().items():
            # print(square, piece)
            piece_value = 0.0
            if piece.piece_type == chess.PAWN:
                piece_value = self._evaluate_pawn(board, square, piece)
            elif piece.piece_type == chess.KNIGHT:
                piece_value = 30.0
            elif piece.piece_type == chess.BISHOP:
                piece_value = 30.0
            elif piece.piece_type == chess.ROOK:
                piece_value = self._evaluate_rook(board, square, piece)
            elif piece.piece_type == chess.QUEEN:
                piece_value = self._evaluate_queen(board, square, piece)
            if color_to_play is piece.color:
                material_value += piece_value
            else:
                material_value -= piece_value

        evaluation += material_value
        self._position_table[epd_key] = evaluation

        # if board.is_check() and board.turn == color_to_play:
        #     evaluation -= 100.0
        # elif board.is_check() and board.turn != color_to_play:
        #     evaluation += 100.0

        return EvalReturnType(
            move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
            eval=evaluation,
            line=line,
        )

    def _evaluate_pawn(
        self, board: chess.Board, square: chess.Square, piece: chess.Piece
    ) -> float:
        return 10.0 * PAWN_EVAL_DICT[piece.color][square]

    def _evaluate_rook(
        self, board: chess.Board, square: chess.Square, piece: chess.Piece
    ) -> float:
        file = chess.square_file(square)
        open_file = True

        # # Check for file being open
        for i in range(0, 7):
            square_to_check = chess.square(file, i)
            if square_to_check == square:
                continue
            else:
                piece_in_way = board.piece_at(square_to_check)
                if piece_in_way is None:
                    continue
                if piece_in_way.color != piece.color or (
                    piece_in_way.color == piece.color
                    and piece_in_way.piece_type != chess.QUEEN
                    and piece_in_way.piece_type != chess.ROOK
                ):
                    open_file = False

        eval = 50.0

        if open_file:
            eval = (eval) * 1.25

        eval = eval * ROOK_EVAL_DICT[piece.color][square]

        return eval

    def _evaluate_queen(
        self, board: chess.Board, square: chess.Square, piece: chess.Piece
    ) -> float:
        return 90.0 * QUEEN_EVAL_DICT[piece.color][square]
