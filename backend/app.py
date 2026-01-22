from flask import Flask, request, jsonify
from flask_cors import CORS
from chess_engine import ChessEngine

app = Flask(__name__)
CORS(app)
game = ChessEngine()
captured_pieces = [] # Empty list to track captured pieces

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({'board_state': game.get_board_state()})

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    move_uci = data['move']
    success = game.make_move(move_uci)
    if success:
        return jsonify({'status': 'success', 'board_state': game.get_board_state()})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid move'})
    
# @app.route('/legal_moves', methods=['GET'])
# def legal_moves():
#     moves = [move.uci() for move in game.board.legal_moves]
#     return jsonify({'legal_moves': moves})

@app.route('/captured-pieces', methods=['GET'])
def captured_pieces():
    return jsonify({'captured-pieces': game.get_captured_pieces()})

@app.route('/reset', methods=['POST'])
def reset_game():
    global game
    game = ChessEngine()
    return jsonify({'status': 'success', 'board_state': game.get_board_state()})

@app.route('/is_game_over', methods=['GET'])
def is_game_over():
    return jsonify({'is_game_over': game.is_game_over()})

if __name__ == '__main__':
    app.run(debug=True)