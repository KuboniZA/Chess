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

    def is_game_over(self) -> bool:
        return self.board.is_game_over()