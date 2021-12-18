from pychess_ai.algos import BaseChessAlgo
import chess


class MiniMaxABP(BaseChessAlgo):
    BASE_ALPHA_VAL = -9999
    BASE_BETA_VAL = 9999

    def __init__(self, depth: int):
        super().__init__(depth)

    def get_next_move(
        self, board: chess.Board, color_to_play: chess.Color
    ) -> chess.Move:
        return self._minimaxabp_root_node(board, color_to_play)

    def _minimaxabp_root_node(
        self, board: chess.Board, color_to_play: chess.Color
    ) -> chess.Move:
        """Root for minimax"""

        best_move = ""
        best_eval = -9999

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
                # print(move, eval)
                if eval > best_eval:
                    best_eval = eval
                    best_move = move

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
    ) -> float:
        if board.is_checkmate():
            return self._evaluator.evaluate(board, num_moves, color_to_play)

        if depth == 0:
            return self._quiescence_search(board, alpha, beta, num_moves, color_to_play)

        # Set the eval to either very large negative of very large positive
        if is_maximizing:
            best_move = -9999
        else:
            best_move = 9999

        # Let's make a move deque to sort it so checks and captures are front of the list
        # Also going to make a hokey dictionary for storing capture moves...since there's a generate function
        # Honestly not sure if that generate function is quick...
        legal_moves = self.generate_check_capture_move_list_order(board)

        # let's step through each legal move
        while legal_moves:
            move = legal_moves.popleft()
            if is_maximizing:
                board.push(move)
                best_move = max(
                    best_move,
                    self._minimaxabp_sub_nodes(
                        board,
                        depth - 1,
                        num_moves + 1,
                        not is_maximizing,
                        alpha,
                        beta,
                        color_to_play,
                    ),
                )
                board.pop()
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    break

            else:
                board.push(move)
                best_move = min(
                    best_move,
                    self._minimaxabp_sub_nodes(
                        board,
                        depth - 1,
                        num_moves + 1,
                        not is_maximizing,
                        alpha,
                        beta,
                        color_to_play,
                    ),
                )
                board.pop()
                beta = min(beta, best_move)
                if beta <= alpha:
                    break

        return best_move

    def _quiescence_search(
        self,
        board: chess.Board,
        alpha: int,
        beta: int,
        num_moves: int,
        color_to_play: chess.Color,
    ) -> float:

        eval = self._evaluator.evaluate(board, num_moves, color_to_play)

        if eval >= beta:
            return beta
        if eval < alpha:
            alpha = eval
        legal_moves = self.generate_check_capture_move_list_order(board, True)

        while legal_moves:
            next_move = legal_moves.popleft()
            board.push(next_move)
            eval = self._quiescence_search(
                board, alpha, beta, num_moves + 1, color_to_play
            )
            board.pop()
            if eval >= beta:
                return beta
            else:
                alpha = eval

        return alpha
