import chess

# fmt: off
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
# fmt: on


class Evaluator:
    def __init__(self):
        self._position_table = dict()
        pass

    def evaluate(
        self, board: chess.Board, num_moves: int, color_to_play: chess.Color
    ) -> float:
        """Chess position evaluation function

        Args:
            board (chess.Board): A python-chess board
            num_moves (int): How many moves deep are we int the evaluation
            color_to_play (chess.Color): What color are we evaluating for at the root

        Returns:
            float: The evaluation
        """

        # Gonna use the FEN without the turn
        epd_key = board.epd()
        if epd_key in self._position_table:
            return self._position_table[epd_key]

        evaluation = 0.0
        if board.is_checkmate():
            return 1000.0 - num_moves

        material_value = 0.0
        for square, piece in board.piece_map().items():
            # print(square, piece)
            piece_value = 0.0
            if piece.piece_type == chess.PAWN:
                piece_value = 10.0
            elif piece.piece_type == chess.KNIGHT:
                piece_value = 30.0
            elif piece.piece_type == chess.BISHOP:
                piece_value = 30.0
            elif piece.piece_type == chess.ROOK:
                piece_value = self._evaluate_rook(board, square, piece)
            elif piece.piece_type == chess.QUEEN:
                piece_value = 90.0
            if color_to_play is piece.color:
                material_value += piece_value
            else:
                material_value -= piece_value

        evaluation += material_value
        self._position_table[epd_key] = evaluation
        return evaluation

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
