from flask import Blueprint, request, jsonify
from domaine.repositories import ParieurRepository
from domaine.modeles import Parieur
from decimal import Decimal

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


@pari_bp.route('/parieur/<int:id_utilisateur>/update_cagnotte', methods=['POST'])
def update_cagnotte(id_utilisateur):
    try:
        data = request.get_json()
        montant = data.get('montant')

        if montant is None:
            return jsonify({"error": "Montant manquant."}), 400

        cagnotte_actuelle = ParieurRepository.get_cagnotte_by_user_id(id_utilisateur)
        if cagnotte_actuelle is None:
            return jsonify({"error": "Parieur non trouvé."}), 404

        montant_decimal = Decimal(montant)
        nouvelle_cagnotte = cagnotte_actuelle + montant_decimal

        if nouvelle_cagnotte < 0:
            return jsonify({
                "error": "Solde insuffisant.",
                "cagnotte_actuelle": float(cagnotte_actuelle)
            }), 400

        ParieurRepository.update_cagnotte(id_utilisateur, nouvelle_cagnotte)

        return jsonify({"success": True, "nouvelle_cagnotte": float(nouvelle_cagnotte)}), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour de la cagnotte : {str(e)}"}), 500
