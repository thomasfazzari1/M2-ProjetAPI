import os
import requests
from flask import Blueprint, request, jsonify, session

authentification_bp = Blueprint('authentification', __name__)

AUTHENTIFICATION_SERVICE_URL = os.getenv('AUTHENTIFICATION_SERVICE_URL')
MATCH_SERVICE_URL = os.getenv('MATCH_SERVICE_URL')
PARI_SERVICE_URL = os.getenv('PARI_SERVICE_URL')


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
        user_id = user_data['id']

        if user_data['is_bookmaker']:
            bookmaker = requests.get(f"{MATCH_SERVICE_URL}/bookmaker/{user_id}")
            if bookmaker.status_code == 404:
                create = requests.post(
                    f"{MATCH_SERVICE_URL}/create_bookmaker",
                    json={
                        "id_utilisateur": user_id
                    }
                )
                if create.status_code != 201:
                    return jsonify({"error": "Échec de la création du profil bookmaker"}), 500

        else:
            parieur = requests.get(f"{PARI_SERVICE_URL}/parieur/{user_id}")
            if parieur.status_code == 404:
                create = requests.post(
                    f"{PARI_SERVICE_URL}/create_parieur",
                    json={
                        "id_utilisateur": user_id,
                        "cagnotte": 0.00
                    }
                )
                if create.status_code != 201:
                    return jsonify({"error": "Échec de la création du profil parieur"}), 500

        return jsonify({
            "user_id": user_data['id'],
            "pseudo": user_data['pseudo'],
            "is_bookmaker": user_data['is_bookmaker']
        }), 200
    else:
        return jsonify({"error": "Connexion échouée"}), response.status_code


@authentification_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Déconnexion réussie"}), 200


@authentification_bp.route('/espace_bookmaker', methods=['GET'])
def espace_bookmaker():
    return jsonify({"success": True}), 200
