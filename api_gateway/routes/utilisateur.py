import os
import requests
from flask import Blueprint, request, jsonify, session

utilisateur_bp = Blueprint('utilisateur', __name__)
UTILISATEUR_SERVICE_URL = os.getenv('UTILISATEUR_SERVICE_URL', 'http://utilisateur:5000')


@utilisateur_bp.route('/create_user', methods=['POST'])
def create_user():
    response = requests.post(f"{UTILISATEUR_SERVICE_URL}/create_user", json=request.get_json())
    return jsonify(response.json()), response.status_code


@utilisateur_bp.route('/login', methods=['POST'])
def login():
    response = requests.post(f"{UTILISATEUR_SERVICE_URL}/login", json=request.get_json())

    if response.status_code == 200:
        user_data = response.json()
        return jsonify({
            "user_id": user_data['id'],
            "pseudo": user_data['pseudo'],
            "is_bookmaker": user_data.get('bookmaker', False)
        }), 200
    else:
        return jsonify({"error": "Connexion échouée"}), 401


@utilisateur_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Déconnexion réussie"}), 200
