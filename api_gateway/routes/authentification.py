import os
import requests
from flask import Blueprint, request, jsonify, session

authentification_bp = Blueprint('authentification', __name__)
AUTHENTIFICATION_SERVICE_URL = os.getenv('AUTHENTIFICATION_SERVICE_URL')

MATCH_SERVICE_URL = os.getenv('MATCH_SERVICE_URL')


@authentification_bp.route('/create_user', methods=['POST'])
def create_user():
    response = requests.post(f"{AUTHENTIFICATION_SERVICE_URL}/create_user", json=request.get_json())
    return jsonify(response.json()), response.status_code


@authentification_bp.route('/login', methods=['POST'])
def login():
    response = requests.post(f"{AUTHENTIFICATION_SERVICE_URL}/login", json=request.get_json())

    if response.status_code == 200:
        user_data = response.json()

        user_data['is_bookmaker'] = user_data.get('bookmaker', False)

        if user_data.get('is_bookmaker', False):
            user_id = user_data['id']

            match_response = requests.get(f"{MATCH_SERVICE_URL}/bookmaker/{user_id}")

            if match_response.status_code == 404:  # Le bookmaker n'existe pas, donc on le crée
                create_response = requests.post(
                    f"{MATCH_SERVICE_URL}/create_bookmaker",
                    json={
                        "pseudo": user_data['pseudo'],
                        "id_utilisateur": user_data['id']
                    }
                )

                if create_response.status_code != 201:
                    return jsonify({"error": "Échec de la création du bookmaker"}), 500

        return jsonify({
            "user_id": user_data['id'],
            "pseudo": user_data['pseudo'],
            "is_bookmaker": user_data['is_bookmaker']
        }), 200
    else:
        return jsonify({"error": "Connexion échouée"}), 401


@authentification_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Déconnexion réussie"}), 200


@authentification_bp.route('/espace_bookmaker', methods=['GET'])
def espace_bookmaker():
    return jsonify({"success": True}), 200
