from algos import BaseChessAlgo
import chess

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
