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


@utilisateur_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    mdp = data.get("mdp")

    if not email or not mdp:
        return jsonify({"error": "Email ou mot de passe manquant."}), 400

    utilisateur = UtilisateurRepository.find_by_email(email)
    if utilisateur and bcrypt.checkpw(mdp.encode('utf-8'), utilisateur['mdp_hash'].encode('utf-8')):
        return jsonify({
            "id": utilisateur['id'],
            "pseudo": utilisateur['pseudo'],
            "bookmaker": utilisateur['bookmaker']
        }), 200

    return jsonify({"error": "Email ou mot de passe incorrect."}), 401


@utilisateur_bp.route('/espace_bookmaker', methods=['GET'])
def espace_bookmaker():
    return jsonify({}), 200
