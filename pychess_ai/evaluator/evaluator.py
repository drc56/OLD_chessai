import chess


class Evaluator:
    def __init__(self):
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
                # print(piece_in_way.piece_type)
                if piece_in_way.color != piece.color or (
                    piece_in_way.color == piece.color
                    and piece_in_way.piece_type != chess.QUEEN
                    and piece_in_way.piece_type != chess.ROOK
                ):
                    open_file = False

        eval = 50.0

        if open_file:
            eval = (eval) * 1.25

        return eval
