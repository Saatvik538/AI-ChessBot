import copy
import random
from board import Board
from move import Move
from const import *
from multiprocessing import Pool, cpu_count

class ChessEngine:
    def __init__(self, depth=3):
        self.depth = depth

    def evaluate_board(self, board):
        total_evaluation = 0
        for row in board.squares:
            for square in row:
                if square.has_piece():
                    piece = square.piece
                    total_evaluation += piece.value
        return total_evaluation

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if board.squares[row][col].has_piece():
                        piece = board.squares[row][col].piece
                        if piece.color == 'white':
                            board.calc_moves(piece, row, col)
                            for move in piece.moves:
                                new_board = copy.deepcopy(board)
                                new_board.move(piece, move)
                                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                                max_eval = max(max_eval, eval)
                                alpha = max(alpha, eval)
                                if beta <= alpha:
                                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if board.squares[row][col].has_piece():
                        piece = board.squares[row][col].piece
                        if piece.color == 'black':
                            board.calc_moves(piece, row, col)
                            for move in piece.moves:
                                new_board = copy.deepcopy(board)
                                new_board.move(piece, move)
                                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                                min_eval = min(min_eval, eval)
                                beta = min(beta, eval)
                                if beta <= alpha:
                                    break
            return min_eval

    def minimax_wrapper(self, board, piece, move, depth, alpha, beta, maximizing_player):
        new_board = copy.deepcopy(board)
        new_board.move(piece, move)
        eval = self.minimax(new_board, depth, alpha, beta, maximizing_player)
        return eval, move, piece

    def get_best_move(self, board, color):
        best_move = None
        best_piece = None
        best_value = float('-inf') if color == 'white' else float('inf')
        maximizing_player = color == 'black'

        all_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.color == color:
                        board.calc_moves(piece, row, col)
                        for move in piece.moves:
                            all_moves.append((board, piece, move, self.depth - 1, float('-inf'), float('inf'), maximizing_player))

        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(self.minimax_wrapper, all_moves)

        for eval, move, piece in results:
            if color == 'white':
                if eval > best_value:
                    best_value = eval
                    best_move = move
                    best_piece = piece
            else:
                if eval < best_value:
                    best_value = eval
                    best_move = move
                    best_piece = piece

        return best_piece, best_move
