from flask import Blueprint, request, jsonify
from domaine.repositories import SportRepository, EvenementRepository, EquipeRepository, MatchRepository, \
    BookmakerRepository
from domaine.modeles import Sport, Evenement, Equipe, Match, Bookmaker

match_bp = Blueprint('match', __name__)


# region Sport
@match_bp.route('/create_sport', methods=['POST'])
def create_sport():
    data = request.get_json()
    nom = data.get("nom")

    if not nom:
        return jsonify({"error": "Le nom ne peut pas être nul."}), 400

    if SportRepository.get_by_name(nom):
        return jsonify({"error": "Un sport avec ce nom existe déjà."}), 400

    try:
        sport = Sport(nom=nom)
        sport_id = SportRepository.create(sport)

        if sport_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création du sport."}), 500

        return jsonify({"success": True, "message": "Sport créé avec succès.", "sport_id": sport_id}), 201

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur."}), 500


@match_bp.route('/get_all_sports', methods=['GET'])
def get_all_sports():
    sports = SportRepository.get_all_sports()
    return jsonify(sports), 200


@match_bp.route('/delete_sport', methods=['POST'])
def delete_sport():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée fournie."}), 400

        sport_id = data.get("sport_id")
        if not sport_id:
            return jsonify({"error": "L'ID du sport est manquant."}), 400

        supprimes = SportRepository.delete(sport_id)
        if supprimes == 0:
            return jsonify({"error": "Sport non trouvé."}), 404

        return jsonify({"success": True, "message": "Sport supprimé avec succès."}), 200

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur."}), 500


# endregion

# region Evenement
@match_bp.route('/create_evenement', methods=['POST'])
def create_evenement():
    data = request.get_json()
    nom = data.get("nom")
    id_sport_associe = data.get("id_sport_associe")

    if not nom or not id_sport_associe:
        return jsonify({"error": "Certains champs sont nuls."}), 400

    sport = SportRepository.get_by_id(id_sport_associe)
    if not sport:
        return jsonify({"error": f"Aucun sport trouvé avec l'ID {id_sport_associe}."}), 404

    evenement_existant = EvenementRepository.get_by_name_and_sport(nom, id_sport_associe)
    if evenement_existant:
        return jsonify({"error": "Un événement avec ce nom existe déjà pour ce sport."}), 400

    try:
        evenement = Evenement(nom=nom, id_sport_associe=id_sport_associe)
        evenement_id = EvenementRepository.create(evenement)

        if evenement_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création de l'évènement."}), 500

        return jsonify({"success": True, "message": "Evènement créé avec succès.", "evenement_id": evenement_id}), 201

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur."}), 500


@match_bp.route('/get_all_evenements', methods=['GET'])
def get_all_evenements():
    evenements = EvenementRepository.get_all_evenements()
    return jsonify(evenements), 200


@match_bp.route('/delete_evenement', methods=['POST'])
def delete_evenement():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée fournie."}), 400

        evenement_id = data.get("evenement_id")
        if not evenement_id:
            return jsonify({"error": "L'ID de l'évènement est manquant."}), 400

        supprimes = EvenementRepository.delete(evenement_id)
        if supprimes == 0:
            return jsonify({"error": "Evenement non trouvé."}), 404

        return jsonify({"success": True, "message": "Evenement supprimé avec succès."}), 200

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur."}), 500


# endregion

# region Equipe
@match_bp.route('/create_equipe', methods=['POST'])
def create_equipe():
    data = request.get_json()
    nom = data.get("nom")
    id_sport_associe = data.get("id_sport_associe")

    if not nom or not id_sport_associe:
        return jsonify({"error": "Certains champs sont nuls."}), 400

    sport = SportRepository.get_by_id(id_sport_associe)
    if not sport:
        return jsonify({"error": f"Aucun sport trouvé avec l'ID {id_sport_associe}."}), 404

    existe = EquipeRepository.get_by_name(nom)
    if existe:
        return jsonify({"error": "Une équipe avec ce nom existe déjà."}), 400

    try:
        equipe = Equipe(nom=nom, id_sport_associe=id_sport_associe)
        equipe_id = EquipeRepository.create(equipe)

        if equipe_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création de l'équipe."}), 500

        return jsonify({"success": True, "message": "Equipe créée avec succès.", "equipe_id": equipe_id}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur interne du serveur : {str(e)}"}), 500


@match_bp.route('/get_all_equipes', methods=['GET'])
def get_all_equipes():
    equipes = EquipeRepository.get_all_equipes()
    return jsonify(equipes), 200


@match_bp.route('/delete_equipe', methods=['POST'])
def delete_equipe():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée fournie."}), 400

        equipe_id = data.get("equipe_id")
        if not equipe_id:
            return jsonify({"error": "L'ID de l'équipe est manquant."}), 400

        supprimes = EquipeRepository.delete(equipe_id)
        if supprimes == 0:
            return jsonify({"error": "Equipe non trouvée."}), 404

        return jsonify({"success": True, "message": "Equipe supprimée avec succès."}), 200

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur."}), 500


# endregion

# region Match
@match_bp.route('/create_match', methods=['POST'])
def create_match():
    data = request.get_json()
    champs = [
        "id_sport", "id_evenement", "date", "heure_debut", "heure_fin",
        "id_eq_domicile", "valeur_cote_domicile", "id_eq_exterieure",
        "valeur_cote_exterieure", "valeur_cote_match_nul", "id_bookmaker"
    ]

    for champ in champs:
        if champ not in data:
            return jsonify({"error": f"Le champ {champ} est requis."}), 400

    try:
        sport = SportRepository.get_by_id(data["id_sport"])
        if not sport:
            return jsonify({"error": f"Aucun sport trouvé avec l'ID {data['id_sport']}."}), 404

        evenement = EvenementRepository.get_by_id(data["id_evenement"])
        if not evenement:
            return jsonify({"error": f"Aucun événement trouvé avec l'ID {data['id_evenement']}."}), 404

        equipe_domicile = EquipeRepository.get_by_id(data["id_eq_domicile"])
        if not equipe_domicile:
            return jsonify({"error": f"Aucune équipe trouvée avec l'ID domicile {data['id_eq_domicile']}."}), 404

        equipe_exterieure = EquipeRepository.get_by_id(data["id_eq_exterieure"])
        if not equipe_exterieure:
            return jsonify({"error": f"Aucune équipe trouvée avec l'ID extérieure {data['id_eq_exterieure']}."}), 404

        bookmaker = BookmakerRepository.get_by_user_id(data["id_bookmaker"])
        if not bookmaker:
            return jsonify(
                {"error": f"Aucun bookmaker trouvé pour l'utilisateur avec l'ID {data['id_bookmaker']}."}), 404

        match = Match(
            id_sport_associe=data["id_sport"],
            id_evenement_associe=data["id_evenement"],
            date=data["date"],
            heure_debut=data["heure_debut"],
            heure_fin=data["heure_fin"],
            id_eq_domicile=data["id_eq_domicile"],
            valeur_cote_domicile=data["valeur_cote_domicile"],
            id_eq_exterieure=data["id_eq_exterieure"],
            valeur_cote_exterieure=data["valeur_cote_exterieure"],
            valeur_cote_match_nul=data["valeur_cote_match_nul"],
            created_by=bookmaker['id'],
            updated_by=bookmaker['id'],
            est_mis_en_avant=data.get("est_mis_en_avant", False)
        )

        match_id = MatchRepository.create(match)

        if match_id is None:
            return jsonify({"success": False, "message": "Erreur lors de la création du match."}), 500

        return jsonify({"success": True, "message": "Match créé avec succès.", "match_id": match_id}), 201

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur."}), 500


@match_bp.route('/get_all_matchs', methods=['GET'])
def get_all_matchs():
    matchs = MatchRepository.get_all_matchs()
    return jsonify(matchs), 200


# endregion

# region Bookmaker
@match_bp.route('/bookmaker/<int:user_id>', methods=['GET'])
def get_bookmaker(user_id):
    bookmaker = BookmakerRepository.get_by_user_id(user_id)
    if not bookmaker:
        return jsonify({"error": "Bookmaker introuvable"}), 404
    return jsonify({
        "id": bookmaker['id']
    }), 200


@match_bp.route('/create_bookmaker', methods=['POST'])
def create_bookmaker():
    data = request.get_json()

    id_utilisateur = data.get("id_utilisateur")

    if not id_utilisateur:
        return jsonify({"error": "Données incomplètes"}), 400

    try:
        bookmaker = Bookmaker(id_utilisateur=id_utilisateur)
        bookmaker_id = BookmakerRepository.create(bookmaker)

        return jsonify({"success": True, "bookmaker_id": bookmaker_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# endregion
