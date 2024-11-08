from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

UTILISATEUR_SERVICE_URL = 'http://utilisateur:5000'

@app.route('/users', methods=['POST'])
def create_user():
    response = requests.post(f"{UTILISATEUR_SERVICE_URL}/create_user", json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    response = requests.get(f"{UTILISATEUR_SERVICE_URL}/users/{user_id}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
