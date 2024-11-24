from flask import Blueprint, request, jsonify
from domaine.repositories import PayeurRepository, PaiementRepository
from domaine.modeles import Payeur, Paiement
from datetime import datetime

paiement_bp = Blueprint('paiement', __name__)


@paiement_bp.route('/paiement/traiter_paiement', methods=['POST'])
def traiter_paiement():
    data = request.get_json()
    print(f"Requête reçue : {data}", flush=True)

    id_utilisateur = data.get("id_utilisateur")
    montant = data.get("montant")
    numero_carte = data.get("numero_carte")
    expiration = data.get("expiration")
    cvc = data.get("cvc")

    if not all([id_utilisateur, montant, numero_carte, expiration, cvc]):
        print("Données de paiement incomplètes", flush=True)
        return jsonify({"error": "Données de paiement incomplètes."}), 400

    try:
        print(f"Recherche du payeur pour id_utilisateur={id_utilisateur}", flush=True)
        payeur = PayeurRepository.get_by_user_id(id_utilisateur)
        if not payeur:
            print(f"Payeur non trouvé pour id_utilisateur={id_utilisateur}", flush=True)
            return jsonify({"error": "Profil de payeur non trouvé."}), 404

        id_payeur = payeur[0]
        print(f"ID payeur trouvé : {id_payeur}", flush=True)

        statut = "validé" if numero_carte.startswith("4") else "échec"
        print(f"Statut du paiement : {statut}", flush=True)

        paiement = Paiement(
            id_payeur=id_payeur,
            montant=montant,
            date=datetime.now(),
            statut=statut
        )
        PaiementRepository.create(paiement)
        print("Paiement inséré dans la base de données", flush=True)

        if statut == "validé":
            return jsonify({"success": True, "message": f"Paiement de {montant:.2f} € validé."}), 200
        else:
            return jsonify({"success": False, "message": "Paiement refusé."}), 400

    except Exception as e:
        print(f"Erreur lors du traitement du paiement : {str(e)}", flush=True)
        return jsonify({"error": f"Erreur lors du traitement du paiement : {str(e)}"}), 500


@paiement_bp.route('/get_payeur/<int:id_utilisateur>', methods=['GET'])
def get_payeur(id_utilisateur):
    try:
        print(f"Recherche du payeur avec id_utilisateur={id_utilisateur}", flush=True)
        payeur = PayeurRepository.get_by_user_id(id_utilisateur)
        if payeur:
            return jsonify({"success": True, "payeur": payeur}), 200
        else:
            return jsonify({"error": "Profil de payeur non trouvé."}), 404
    except Exception as e:
        print(f"Erreur dans get_payeur : {str(e)}", flush=True)
        return jsonify({"error": f"Erreur lors de la vérification du payeur : {str(e)}"}), 500


@paiement_bp.route('/create_payeur', methods=['POST'])
def create_payeur():
    try:
        data = request.get_json()
        id_utilisateur = data.get("id_utilisateur")

        if not id_utilisateur:
            return jsonify({"error": "ID utilisateur manquant."}), 400

        payeur = PayeurRepository.get_by_user_id(id_utilisateur)
        if payeur:
            return jsonify({"error": "Le profil de payeur existe déjà."}), 400

        payeur_id = PayeurRepository.create(id_utilisateur)
        return jsonify({"success": True, "payeur_id": payeur_id}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création du payeur : {str(e)}"}), 500
