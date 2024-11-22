from flask import Blueprint, request, jsonify
from domaine.repositories import ParieurRepository
from domaine.modeles import Parieur

pari_bp = Blueprint('pari', __name__)


@pari_bp.route('/create_parieur', methods=['POST'])
def create_parieur():
    data = request.get_json()

    id_utilisateur = data.get("id_utilisateur")
    cagnotte = data.get("cagnotte", 0.00)

    if not id_utilisateur:
        return jsonify({"error": "Données incomplètes : id_utilisateur manquant"}), 400

    try:
        parieur = Parieur(id_utilisateur=id_utilisateur, cagnotte=cagnotte)
        parieur_id = ParieurRepository.create(parieur)

        return jsonify({"success": True, "parieur_id": parieur_id}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création du parieur : {str(e)}"}), 500


@pari_bp.route('/parieur/<int:id_utilisateur>/cagnotte', methods=['GET'])
def get_cagnotte(id_utilisateur):
    try:
        cagnotte = ParieurRepository.get_cagnotte_by_user_id(id_utilisateur)
        if cagnotte is not None:
            return jsonify({"cagnotte": float(cagnotte)}), 200
        else:
            return jsonify({"error": "Parieur non trouvé."}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération de la cagnotte : {str(e)}"}), 500
