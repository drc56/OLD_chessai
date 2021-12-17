#!/usr/bin/python3
from abc import ABC, abstractmethod
from collections import deque, OrderedDict
from enum import Enum
from timeit import default_timer as timer
import chess


class Algo(Enum):
    """Enum for selecting which algorithm to run
    """
    ABP = 0
    NO_ABP = 1


class Evaluator():
    def __init__(self):
        pass

    def evaluate(self, board: chess.Board, num_moves: int, color_to_play: chess.Color) -> float:
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

    def _evaluate_rook(self, board: chess.Board, square: chess.Square, piece: chess.Piece) -> float:
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
                if piece_in_way.color != piece.color or (piece_in_way.color == piece.color and piece_in_way.piece_type != chess.QUEEN and piece_in_way.piece_type != chess.ROOK):
                    open_file = False

        eval = 50.0

        if open_file:
            eval = (eval) * 1.25

        return eval


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


class MiniMax(BaseChessAlgo):
    def __init__(self, depth: int):
        super().__init__(depth)

    def get_next_move(self, board: chess.Board, color_to_play: chess.Color) -> chess.Move:
        return self._minimax_root_node(board, color_to_play)

    def _minimax_root_node(self, board: chess.Board, color_to_play: chess.Color) -> chess.Move:
        """Root for minimax
        """

        best_move = ""
        best_eval = -9999

        # Generate a list of all legal moves
        legal_moves = self.generate_check_capture_move_list_order(board)

        # We also start as the maximizing player as we are making the move
        is_maximizing = True

        # let's step through each legal move
        while(legal_moves):
            move = legal_moves.popleft()
            if(is_maximizing):
                board.push(move)
                eval = self._minimax_sub_nodes(board, self._depth, 0,
                                               not is_maximizing, color_to_play)
                board.pop()
                # print(move, eval)
                if(eval > best_eval):
                    best_eval = eval
                    best_move = move

        return best_move

    def _minimax_sub_nodes(self, board: chess.Board, depth: int, num_moves: int, is_maximizing: bool, color_to_play: chess.Color) -> float:
        if(depth == 0 or board.is_checkmate()):
            return self._evaluator.evaluate(board, num_moves, color_to_play)

        # Generate a list of all legal moves to play in this position
        legal_moves = board.generate_legal_moves()

        # Set the eval to either very large negative of very large positive
        if(is_maximizing):
            best_move = -9999
        else:
            best_move = 9999

        # let's step through each legal move
        for move in legal_moves:
            if(is_maximizing):
                board.push(move)
                best_move = max(best_move, self._minimax_sub_nodes(
                    board, depth-1, num_moves+1, not is_maximizing, color_to_play))
                board.pop()

            else:
                board.push(move)
                best_move = min(best_move, self._minimax_sub_nodes(
                    board, depth-1, num_moves+1, not is_maximizing, color_to_play))
                board.pop()

        return best_move


class MiniMaxABP(BaseChessAlgo):
    BASE_ALPHA_VAL = -9999
    BASE_BETA_VAL = 9999

    def __init__(self, depth: int):
        super().__init__(depth)

    def get_next_move(self, board: chess.Board, color_to_play: chess.Color) -> chess.Move:
        return self._minimaxabp_root_node(board, color_to_play)

    def _minimaxabp_root_node(self, board: chess.Board, color_to_play: chess.Color) -> chess.Move:
        """Root for minimax
        """

        best_move = ""
        best_eval = -9999

        # Generate a list of all legal moves
        legal_moves = self.generate_check_capture_move_list_order(board)

        # We also start as the maximizing player as we are making the move
        is_maximizing = True

        # let's step through each legal move
        while(legal_moves):
            move = legal_moves.popleft()
            if(is_maximizing):
                board.push(move)
                eval = self._minimaxabp_sub_nodes(
                    board, self._depth, 0, not is_maximizing, self.BASE_ALPHA_VAL, self.BASE_BETA_VAL, color_to_play)
                board.pop()
                # print(move, eval)
                if(eval > best_eval):
                    best_eval = eval
                    best_move = move

        return best_move

    def _minimaxabp_sub_nodes(self, board: chess.Board, depth: int, num_moves: int, is_maximizing: bool, alpha: int, beta: int, color_to_play: chess.Color) -> float:
        if(depth == 0 or board.is_checkmate()):
            return self._evaluator.evaluate(board, num_moves, color_to_play)

        # Set the eval to either very large negative of very large positive
        if(is_maximizing):
            best_move = -9999
        else:
            best_move = 9999

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

        # let's step through each legal move
        while legal_moves:
            move = legal_moves.popleft()
            if(is_maximizing):
                board.push(move)
                best_move = max(best_move, self._minimaxabp_sub_nodes(
                    board, depth-1, num_moves+1, not is_maximizing, alpha, beta, color_to_play))
                board.pop()
                alpha = max(alpha, best_move)
                if(beta <= alpha):
                    break

            else:
                board.push(move)
                best_move = min(best_move, self._minimaxabp_sub_nodes(
                    board, depth-1, num_moves+1, not is_maximizing,  alpha, beta,  color_to_play))
                board.pop()
                beta = min(beta, best_move)
                if(beta <= alpha):
                    break

        return best_move


class ChessAi:
    def __init__(self, algo_type: Algo, depth: int = 3, starting_fen: str = None) -> None:
        if str is None:
            self._board = chess.Board()
        else:
            self._board = chess.Board(fen=starting_fen)

        if algo_type == Algo.ABP:
            self._ai = MiniMaxABP(depth)
        elif(algo_type == Algo.NO_ABP):
            self._ai = MiniMax(depth)
    
    def update_with_move(self, move : chess.Move):
        # TODO (dan) At some point make this check legal moves, but for now we'll control that  
        self._board.push(move)

    def take_turn(self, color : chess.Color) -> str:
        next_move = self.get_next_move(color)
        self._board.push(next_move)
        print(self._board)
        return next_move
    
    def get_next_move(self, color : chess.Color) -> str:
        return self._ai.get_next_move(self._board, color)
    
    def print_board(self) -> None:
        print(self._board)


def main():
    # board_fen_string = "3k4/8/1q5p/8/8/4B3/7R/4K3 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # next_move = runminimax(board, 1, chess.WHITE, Algo.ABP)
    # print(next_move)
    # board.push(next_move)
    # print(board)

    # print("------")

    # board_fen_string = "3k4/7R/1q5p/8/8/4B3/6Q1/4K3 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # next_move = runminimax(board, 3, chess.WHITE, Algo.ABP)
    # print(next_move)
    # board.push(next_move)
    # print(board)

    # print("------")

    # board_fen_string = "1q4k1/5ppp/8/8/3BQ3/8/8/4RK2 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # next_move = runminimax(board, 3, chess.WHITE, Algo.ABP)
    # print(next_move)
    # board.push(next_move)
    # print(board)

    print("------")

    board_fen_string = "4r1k1/5ppp/4q3/5b2/8/8/5PPP/1Q4K1 b - - 0 1"
    chess_ai = ChessAi(Algo.ABP, 3, board_fen_string)
    chess_ai.print_board()
    start = timer()
    next_move = chess_ai.take_turn(chess.BLACK)
    end = timer()
    print("ABP Time : {} ABP Move : {}".format((end-start), next_move))

    print("------")

    board_fen_string = "4r1k1/5ppp/4q3/5b2/8/8/5PPP/1Q4K1 b - - 0 1"
    chess_ai = ChessAi(Algo.NO_ABP, 3, board_fen_string)
    chess_ai.print_board()
    start = timer()
    next_move = chess_ai.take_turn(chess.BLACK)
    end = timer()
    print("ABP Time : {} ABP Move : {}".format((end-start), next_move))

    # board_fen_string = "4rk2/p4ppp/1p2p3/3p4/3P4/1P2P3/P4PPP/4RK2 w - - 0 1"
    # board = chess.Board(fen=board_fen_string)
    # print(board)
    # start = timer()
    # next_move = runminimax(board, 5, chess.WHITE, Algo.ABP)
    # end = timer()
    # print("ABP Time : {} ABP Move : {}".format((end-start), next_move))
    # board.push(next_move)
    # print(board)


if __name__ == '__main__':
    main()
