from flask import Blueprint, request, jsonify
import requests
import os

paiement_bp = Blueprint('paiement', __name__)

PAIEMENT_SERVICE_URL = os.getenv('PAIEMENT_SERVICE_URL')
PARI_SERVICE_URL = os.getenv('PARI_SERVICE_URL')


@paiement_bp.route('/paiement/traiter_paiement_recharge', methods=['POST'])
def traiter_paiement_recharge():
    paiement_response = requests.post(
        f"{PAIEMENT_SERVICE_URL}/paiement/traiter_paiement", json=request.json
    )
    if paiement_response.status_code != 200:
        return jsonify(paiement_response.json()), paiement_response.status_code

    paiement_data = request.json
    montant = paiement_data.get("montant")
    id_utilisateur = paiement_data.get("id_utilisateur")

    if montant is not None and id_utilisateur is not None:
        pari_response = requests.post(
            f"{PARI_SERVICE_URL}/parieur/{id_utilisateur}/update_cagnotte",
            json={"montant": montant}
        )
        if pari_response.status_code != 200:
            return jsonify({
                "error": "Paiement effectué, mais échec de la mise à jour de la cagnotte.",
                "details": pari_response.json()
            }), 500

    return jsonify(
        {"success": True, "message": "Paiement et mise à jour de la cagnotte effectués avec succès."}
    ), 200


@paiement_bp.route('/paiement/get_payeur/<int:id_utilisateur>', methods=['GET'])
def get_payeur(id_utilisateur):
    response = requests.get(f"{PAIEMENT_SERVICE_URL}/get_payeur/{id_utilisateur}")
    return jsonify(response.json()), response.status_code


@paiement_bp.route('/paiement/create_payeur', methods=['POST'])
def create_payeur():
    response = requests.post(f"{PAIEMENT_SERVICE_URL}/create_payeur", json=request.json)
    return jsonify(response.json()), response.status_code
