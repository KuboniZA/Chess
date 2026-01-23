import chess

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
    