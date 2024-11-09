from flask import Blueprint, request, jsonify
from domaine.repositories import UtilisateurRepository
from domaine.modeles import Utilisateur

import bcrypt

utilisateur_bp = Blueprint('utilisateur', __name__)


@utilisateur_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    pseudo = data.get("pseudo")
    email = data.get("email")
    mdp = data.get("mdp")

    if not pseudo or not email or not mdp:
        return jsonify({"error": "Certains champs sont nuls."}), 400

    mdp_hash = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    utilisateur = Utilisateur(pseudo=pseudo, email=email, mdp_hash=mdp_hash)

    utilisateur_id = UtilisateurRepository.create(utilisateur)
    return jsonify({"success": True, "message": "Utilisateur créé avec succès.", "user_id": utilisateur_id}), 201
