from dataclasses import dataclass
from collections import deque
from pychess_ai.algos import BaseChessAlgo
from pychess_ai.evaluator import EvalReturnType
import chess


class MiniMaxABP(BaseChessAlgo):
    BASE_ALPHA_VAL = -99999
    BASE_BETA_VAL = 99999

    def __init__(self, depth: int):
        super().__init__(depth)

    @staticmethod
    def make_eval_string(board: chess.Board, move_list: list):
        eval_string = ""
        for item in move_list:
            eval_string += board.san(item) + ","
            board.push(item)
        for i in range(0, len(move_list)):
            board.pop()
        return eval_string

    def get_next_move(
        self, board: chess.Board, color_to_play: chess.Color
    ) -> chess.Move:
        return self._minimaxabp_root_node(board, color_to_play)

    def _minimaxabp_root_node(
        self, board: chess.Board, color_to_play: chess.Color
    ) -> chess.Move:
        """Root for minimax"""

        best_move = ""
        best_eval = -99999
        best_eval_object = None

        # Generate a list of all legal moves
        legal_moves = self.generate_check_capture_move_list_order(board)

        # We also start as the maximizing player as we are making the move
        is_maximizing = True

        # let's step through each legal move
        while legal_moves:
            move = legal_moves.popleft()
            if is_maximizing:
                board.push(move)
                eval = self._minimaxabp_sub_nodes(
                    board,
                    self._depth,
                    0,
                    not is_maximizing,
                    self.BASE_ALPHA_VAL,
                    self.BASE_BETA_VAL,
                    color_to_play,
                )
                board.pop()
                print(
                    "Move: {}, Eval: {}, Line: {}".format(
                        board.san(eval.move),
                        eval.eval,
                        self.make_eval_string(board, eval.line),
                    )
                )
                if eval.eval > best_eval:
                    best_eval = eval.eval
                    best_eval_object = eval
                    best_move = eval.move

        return best_move

    def _minimaxabp_sub_nodes(
        self,
        board: chess.Board,
        depth: int,
        num_moves: int,
        is_maximizing: bool,
        alpha: int,
        beta: int,
        color_to_play: chess.Color,
    ) -> EvalReturnType:
        if board.is_checkmate():
            return self._evaluator.evaluate(board, num_moves, color_to_play)

        if depth == 0:
            return self._evaluator.evaluate(board, num_moves, color_to_play)
            # return self._quiescence_search(board, alpha, beta, num_moves, color_to_play)

        # Set the eval to either very large negative of very large positive
        best_eval = None
        if is_maximizing:
            best_move = -99999
        else:
            best_move = 99999

        # Let's make a move deque to sort it so checks and captures are front of the list
        # Also going to make a hokey dictionary for storing capture moves...since there's a generate function
        # Honestly not sure if that generate function is quick...
        legal_moves = self.generate_check_capture_move_list_order(board)

        # let's step through each legal move
        while legal_moves:
            move = legal_moves.popleft()
            if is_maximizing:
                board.push(move)
                eval = self._minimaxabp_sub_nodes(
                    board,
                    depth - 1,
                    num_moves + 1,
                    not is_maximizing,
                    alpha,
                    beta,
                    color_to_play,
                )
                if eval.eval > best_move:
                    best_move = eval.eval
                    best_eval = eval
                board.pop()
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    break

            else:
                board.push(move)
                eval = self._minimaxabp_sub_nodes(
                    board,
                    depth - 1,
                    num_moves + 1,
                    not is_maximizing,
                    alpha,
                    beta,
                    color_to_play,
                )
                if eval.eval < best_move:
                    best_move = eval.eval
                    best_eval = eval
                board.pop()
                beta = min(beta, best_move)
                if beta <= alpha:
                    break

        # print(alpha, beta)
        return best_eval

    def _quiescence_search(
        self,
        board: chess.Board,
        alpha: int,
        beta: int,
        num_moves: int,
        color_to_play: chess.Color,
    ) -> EvalReturnType:
        eval = self._evaluator.evaluate(board, num_moves, color_to_play)

        # if board.is_check() is False:
        #     if eval.eval >= beta:
        #         return EvalReturnType(
        #             move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
        #             eval=beta,
        #             line=board.move_stack[len(board.move_stack) - (num_moves + 1) :],
        #         )
        #     if eval.eval > alpha:
        #         alpha = eval.eval

        # if board.is_check():
        #     legal_moves = deque(board.generate_legal_moves())
        # else:
        #     legal_moves = self.generate_check_capture_move_list_order(board, True)

        if eval.eval >= beta:
            return EvalReturnType(
                move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
                eval=beta,
                line=board.move_stack[len(board.move_stack) - (num_moves + 1) :],
            )
        if eval.eval > alpha:
            alpha = eval.eval

        legal_moves = self.generate_check_capture_move_list_order(board, True)

        while legal_moves:
            next_move = legal_moves.popleft()
            board.push(next_move)
            eval = self._quiescence_search(
                board, -beta, -alpha, num_moves + 1, color_to_play
            )
            # negate the eval as a part of quiescence_search
            eval.eval = eval.eval * -1.0
            board.pop()
            if eval.eval >= beta:
                # print("here")
                return EvalReturnType(
                    move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
                    eval=beta,
                    line=board.move_stack[len(board.move_stack) - (num_moves + 1) :],
                )
            if eval.eval > alpha:
                alpha = eval.eval
        return EvalReturnType(
            move=board.move_stack[len(board.move_stack) - (num_moves + 1)],
            eval=alpha,
            line=board.move_stack[len(board.move_stack) - (num_moves + 1) :],
        )
