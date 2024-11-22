from flask import Blueprint, request, jsonify
import requests
import os

pari_bp = Blueprint('pari', __name__)
PARI_SERVICE_URL = os.getenv('PARI_SERVICE_URL')


@pari_bp.route('/parieur/<int:id_utilisateur>/cagnotte', methods=['GET'])
def get_cagnotte(id_utilisateur):
    try:
        response = requests.get(f"{PARI_SERVICE_URL}/parieur/{id_utilisateur}/cagnotte")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erreur de communication avec le service pari : {str(e)}"}), 500


@pari_bp.route('/details_cagnotte', methods=['GET', 'POST'])
def details_cagnotte():
    response = requests.post(f"{PARI_SERVICE_URL}/details_cagnotte", json=request.get_json())
    return jsonify(response.json()), response.status_code
