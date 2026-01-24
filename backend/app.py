from flask import Flask, request, jsonify
from flask_cors import CORS
from chess_engine import ChessEngine
import time
import threading

app = Flask(__name__)
CORS(app)
game = ChessEngine()
captured_pieces = [] # Empty list to track captured pieces
game_mode = {
    "white": "human",
    "black": "ai",
    "difficulty": "beginner"
}

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({
        'board_state': game.get_board_state(),
        'turn': 'White' if game.board.turn else 'Black',
        'check': game.board.is_check() if game.board.move_stack else False,
        'checkmate': game.board.is_checkmate() if game.board.move_stack else False
        })

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    move_uci = data['move']
    success = game.make_move(move_uci)
    if success:
        current_turn = "white" if game.board.turn else "black"
        if game_mode[current_turn] == "ai" and not game.board.is_game_over():
            time.sleep(2)
            game.make_computer_move(game_mode["difficulty"])
        return jsonify({
            'status': 'success', 
            'board_state': game.get_board_state(),
            'turn': 'white' if game.board.turn else 'Black',
            'check': game.board.is_check(),
            'checkmate': game.board.is_checkmate()
            })
    else:
        return jsonify({'status': 'error', 'message': 'Invalid move'})
    
# @app.route('/legal_moves', methods=['GET'])
# def legal_moves():
#     moves = [move.uci() for move in game.board.legal_moves]
#     return jsonify({'legal_moves': moves})

@app.route('/captured-pieces', methods=['GET'])
def captured_pieces():
    return jsonify({
        'captured-pieces': game.get_captured_pieces(),
        'white-captured': [p for p in game.get_captured_pieces() if p['color'] == 'white'],
        'black-captured': [p for p in game.get_captured_pieces() if p['color'] == 'black']
        })

@app.route('/reset', methods=['POST'])
def reset_game():
    global game
    game = ChessEngine()
    return jsonify({
        'status': 'success', 
        'board_state': game.get_board_state(),
        'check' : False,
        'checkmate': False
        })

@app.route('/reset-captured', methods=['POST'])
def reset_captured():
    global captured_pieces
    captured_pieces = []
    return jsonify({'status': 'success'})

@app.route('/is_game_over', methods=['GET'])
def is_game_over():
    return jsonify({'is_game_over': game.is_game_over()})

if __name__ == '__main__':
    app.run(debug=True)