from flask import Flask, request, jsonify
from flask_cors import CORS
from chess_engine import ChessEngine

app = Flask(__name__)
CORS(app)
engine = ChessEngine()

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    move_uci = data['move']
    success = engine.make_move(move_uci)
    if success:
        return jsonify({'status': 'success', 'board_state': engine.get_board_state()})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid move'})

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({'board_state': engine.get_board_state()})

@app.route('/is_game_over', methods=['GET'])
def is_game_over():
    return jsonify({'is_game_over': engine.is_game_over()})

if __name__ == '__main__':
    app.run(debug=True)