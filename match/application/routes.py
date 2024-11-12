from flask import Blueprint, request, jsonify
from domaine.repositories import SportRepository
from domaine.modeles import Sport

match_bp = Blueprint('match', __name__)


@match_bp.route('/create_sport', methods=['POST'])
def create_sport():
    data = request.get_json()
    nom = data.get("nom")

    if not nom:
        return jsonify({"error": "Le nom ne peut pas être nul."}), 400

    try:
        sport = Sport(nom=nom)
        sport_id = SportRepository.create(sport)

        if sport_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création du sport."}), 500

        return jsonify({"success": True, "message": "Sport créé avec succès.", "sport_id": sport_id}), 201

    except Exception as e:
        print(f"Erreur lors de la création du sport : {e}")
        return jsonify({"error": "Erreur interne du serveur."}), 500


@match_bp.route('/get_all_sports', methods=['GET'])
def get_all_sports():
    sports = SportRepository.get_all_sports()
    return jsonify(sports), 200
