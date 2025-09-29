from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store status for both users
users = {
    "player1": {"available": False, "last_update": None, "name": "Player 1"},
    "player2": {"available": False, "last_update": None, "name": "Player 2"}
}

@app.route('/')
def home():
    return "PA Status API Running"

@app.route('/status/<user_id>', methods=['GET'])
def get_status(user_id):
    if user_id in users:
        return jsonify(users[user_id])
    return jsonify({"error": "User not found"}), 404

@app.route('/toggle/<user_id>', methods=['POST'])
def toggle_status(user_id):
    if user_id in users:
        users[user_id]["available"] = not users[user_id]["available"]
        users[user_id]["last_update"] = datetime.now().isoformat()
        return jsonify(users[user_id])
    return jsonify({"error": "User not found"}), 404

@app.route('/all_status', methods=['GET'])
def all_status():
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)