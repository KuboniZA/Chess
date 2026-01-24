import chess
import random

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()

    def get_board_state(self):
        pieces = []

        for square, piece in self.board.piece_map().items():
            pieces.append({
                'type': piece.symbol().lower(),
                'color': 'white' if piece.color == chess.WHITE else 'black',
                'position': chess.square_name(square)
            })
        return pieces

    def make_move(self, move_uci: str) -> bool:
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            else:
                return False
        except ValueError:
            return False
        
    def get_captured_pieces(self):
        captured = []
        starting_pieces = {
            'P': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1,
            'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1
        }

        piece_symbols = {
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
        }

        current_pieces = {}

        for piece in self.board.piece_map().values():
            symbol = piece.symbol()
            if symbol in current_pieces:
                current_pieces[symbol] += 1
            else:
                current_pieces[symbol] = 1

        for symbol, count in starting_pieces.items():
            current_count = current_pieces.get(symbol, 0)
            captured_count = count - current_count
            for _ in range(captured_count):
                captured.append({
                    'type': symbol.lower(),
                    'color': 'white' if symbol.isupper() else 'black',
                    'symbol': piece_symbols[symbol] # Added this line along with its array to make captured pieces visible/
                })
        return captured
    
    def make_computer_move(self, difficulty: str):
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return
        
        if difficulty == "beginner":
            move = random.choice(legal_moves)
        elif difficulty == "intermediate":
            captures = [m for m in legal_moves if self.board.is_capture(m)]
            move = random.choice(captures) if captures else random.choice(legal_moves)
        elif difficulty == "hard":
            move = self.minimax_root(depth=2)
        else:
            move = random.choice(legal_moves)

        self.board.push(move)

    def evaluate_board_state(self):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }
        score = 0
        for piece_type, value in values.items():
            score += len(self.board.pieces(piece_type, chess.WHITE)) * value
            score -= len(self.board.pieces(piece_type, chess.BLACK)) * value
        return score
    
    def minimax(self, depth, maximizing):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board_state()
        
        if maximizing:
            max_eval = -9999
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth -1, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
    

