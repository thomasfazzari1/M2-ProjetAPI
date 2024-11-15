from flask import Blueprint, request, jsonify
from domaine.repositories import SportRepository, EvenementRepository, EquipeRepository, MatchRepository
from domaine.modeles import Sport, Evenement, Equipe, Match

match_bp = Blueprint('match', __name__)


# region Sport
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


@match_bp.route('/delete_sport', methods=['POST'])
def delete_sport():
    data = request.get_json()
    sport_id = data.get("sport_id")

    supprimes = SportRepository.delete(sport_id)
    if supprimes == 0:
        return jsonify({"success": False, "message": "Sport non trouvé."}), 404

    return jsonify({"success": True, "message": "Sport supprimé avec succès."}), 200


# endregion

# region Evenement
@match_bp.route('/create_evenement', methods=['POST'])
def create_evenement():
    data = request.get_json()
    nom = data.get("nom")
    id_sport_associe = data.get("id_sport_associe")

    if not nom or not id_sport_associe:
        return jsonify({"error": "Certains champs sont nuls."}), 400

    try:
        evenement = Evenement(nom=nom, id_sport_associe=id_sport_associe)
        evenement_id = EvenementRepository.create(evenement)

        if evenement_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création de l'évènement."}), 500

        return jsonify({"success": True, "message": "Evènement créé avec succès.", "evenement_id": evenement_id}), 201

    except Exception as e:
        print(f"Erreur lors de la création de l'évènement : {e}")
        return jsonify({"error": "Erreur interne du serveur."}), 500


@match_bp.route('/get_all_evenements', methods=['GET'])
def get_all_evenements():
    evenements = EvenementRepository.get_all_evenements()
    return jsonify(evenements), 200


@match_bp.route('/delete_evenement', methods=['POST'])
def delete_evenement():
    data = request.get_json()
    evenement_id = data.get("evenement_id")

    supprimes = EvenementRepository.delete(evenement_id)
    if supprimes == 0:
        return jsonify({"success": False, "message": "Evenement non trouvé."}), 404

    return jsonify({"success": True, "message": "Evenement supprimé avec succès."}), 200


# endregion

# region Equipe
@match_bp.route('/create_equipe', methods=['POST'])
def create_equipe():
    data = request.get_json()
    nom = data.get("nom")
    id_sport_associe = data.get("id_sport_associe")

    if not nom or not id_sport_associe:
        return jsonify({"error": "Certains champs sont nuls."}), 400

    try:
        equipe = Equipe(nom=nom, id_sport_associe=id_sport_associe)
        equipe_id = EquipeRepository.create(equipe)

        if equipe_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création de l'équipe."}), 500

        return jsonify({"success": True, "message": "Equipe créée avec succès.", "equipe_id": equipe_id}), 201

    except Exception as e:
        print(f"Erreur lors de la création de l'équipe : {e}")
        return jsonify({"error": "Erreur interne du serveur."}), 500


@match_bp.route('/get_all_equipes', methods=['GET'])
def get_all_equipes():
    equipes = EquipeRepository.get_all_equipes()
    return jsonify(equipes), 200


@match_bp.route('/delete_equipe', methods=['POST'])
def delete_equipe():
    data = request.get_json()
    equipe_id = data.get("equipe_id")

    supprimes = EquipeRepository.delete(equipe_id)
    if supprimes == 0:
        return jsonify({"success": False, "message": "Equipe non trouvée."}), 404

    return jsonify({"success": True, "message": "Equipe supprimée avec succès."}), 200


# endregion

# region Match
@match_bp.route('/create_match', methods=['POST'])
def create_match():
    data = request.get_json()
    champs = [
        "id_sport", "id_evenement", "date", "heure_debut", "heure_fin",
        "id_eq_domicile", "valeur_cote_eq_domicile", "id_eq_exterieure",
        "valeur_cote_eq_exterieure", "valeur_cote_match_nul", "id_bookmaker"
    ]

    for champ in champs:
        if champ not in data:
            return jsonify({"error": f"Le champ {champ} est requis."}), 400

    try:
        match = Match(
            id_sport_associe=data["id_sport"],
            id_evenement_associe=data["id_evenement"],
            date=data["date"],
            heure_debut=data["heure_debut"],
            heure_fin=data["heure_fin"],
            id_eq_domicile=data["id_eq_domicile"],
            valeur_cote_eq_domicile=data["valeur_cote_eq_domicile"],
            id_eq_exterieure=data["id_eq_exterieure"],
            valeur_cote_eq_exterieure=data["valeur_cote_eq_exterieure"],
            valeur_cote_match_nul=data["valeur_cote_match_nul"],
            id_bookmaker=data["id_bookmaker"],
            est_mis_en_avant=data.get("est_mis_en_avant", False)
        )

        match_id = MatchRepository.create(match)

        if match_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création du match."}), 500

        return jsonify({"success": True, "message": "Match créé avec succès.", "match_id": match_id}), 201

    except Exception as e:
        print(f"Erreur lors de la création du match : {e}")
        return jsonify({"error": "Erreur interne du serveur."}), 500


@match_bp.route('/get_all_matchs', methods=['GET'])
def get_all_matchs():
    matchs = MatchRepository.get_all_matchs()
    return jsonify(matchs), 200
# endregion
