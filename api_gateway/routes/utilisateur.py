from flask import Blueprint, request, jsonify
import requests
import os

utilisateur_bp = Blueprint('utilisateur', __name__)

UTILISATEUR_SERVICE_URL = os.getenv('UTILISATEUR_SERVICE_URL', 'http://utilisateur:5000')

@utilisateur_bp.route('/create_user', methods=['POST'])
def create_user():
    response = requests.post(f"{UTILISATEUR_SERVICE_URL}/create_user", json=request.get_json())
    return jsonify(response.json()), response.status_code
