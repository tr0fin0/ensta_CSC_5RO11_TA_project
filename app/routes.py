# app/routes.py

from flask import Blueprint, request, jsonify
import models



guess_game = Blueprint('guess_game', __name__)

@guess_game.route('/guess-game', methods=['POST'])
def handle_guess_game():
    try:
        data = request.get_json()

        models.add_row_csv(
            data.get('animal'),
            data.get('isGuess'),
            data.get('isGuesser'),
        )

        return jsonify({'status': 'success', 'message': 'Data saved successfully'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
