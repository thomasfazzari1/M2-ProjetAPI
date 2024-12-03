from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

match_bp = Blueprint('match', __name__)


@match_bp.route('/ajouter_sport', methods=['GET', 'POST'])
def ajouter_sport():
    if request.method == 'POST':
        nom = request.form['nom']

        response = requests.post(f"{API_GATEWAY_URL}/create_sport", json={
            "nom": nom
        })

        if response.status_code == 201:
            flash("Sport créé avec succès.", "success")
        else:
            flash("Erreur lors de la création du sport.", "danger")

    response = requests.get(f"{API_GATEWAY_URL}/get_all_sports")
    sports = response.json()

    return render_template('match/ajouter_sport.html', sports=sports)


@match_bp.route('/supprimer_sport/<int:sport_id>', methods=['POST'])
def supprimer_sport(sport_id):
    response = requests.post(f"{API_GATEWAY_URL}/delete_sport", json={
        "sport_id": sport_id
    })

    if response.status_code == 200:
        flash("Sport supprimé avec succès.", "success")
    elif response.status_code == 404:
        flash("Sport non trouvé.", "warning")

    return redirect(url_for('match.ajouter_sport'))


@match_bp.route('/ajouter_evenement', methods=['GET', 'POST'])
def ajouter_evenement():
    if request.method == 'POST':
        nom = request.form['nom']
        id_sport_associe = request.form['id_sport_associe']

        response = requests.post(f"{API_GATEWAY_URL}/create_evenement", json={
            "nom": nom,
            "id_sport_associe": id_sport_associe
        })

        if response.status_code == 201:
            flash("Événement créé avec succès.", "success")
        else:
            flash("Erreur lors de la création de l'événement.", "danger")

    response = requests.get(f"{API_GATEWAY_URL}/get_all_evenements")
    evenements = response.json()

    response = requests.get(f"{API_GATEWAY_URL}/get_all_sports")
    sports = response.json()

    for evenement in evenements:
        sport_associe = next((sport for sport in sports if sport['id'] == evenement['id_sport_associe']), None)
        evenement['sport_nom'] = sport_associe['nom'] if sport_associe else "Sport inconnu"

    return render_template('match/ajouter_evenement.html', sports=sports, evenements=evenements)


@match_bp.route('/supprimer_evenement/<int:evenement_id>', methods=['POST'])
def supprimer_evenement(evenement_id):
    response = requests.post(f"{API_GATEWAY_URL}/delete_evenement", json={
        "evenement_id": evenement_id
    })

    if response.status_code == 200:
        flash("Evenement supprimé avec succès.", "success")
    elif response.status_code == 404:
        flash("Evenement non trouvé.", "warning")

    return redirect(url_for('match.ajouter_evenement'))


@match_bp.route('/ajouter_equipe', methods=['GET', 'POST'])
def ajouter_equipe():
    if request.method == 'POST':
        nom = request.form['nom']
        id_sport_associe = request.form['id_sport_associe']

        response = requests.post(f"{API_GATEWAY_URL}/create_equipe", json={
            "nom": nom,
            "id_sport_associe": id_sport_associe
        })

        if response.status_code == 201:
            flash("Équipe créée avec succès.", "success")
        else:
            flash("Erreur lors de la création de l'équipe.", "danger")

    response = requests.get(f"{API_GATEWAY_URL}/get_all_equipes")
    equipes = response.json()

    response = requests.get(f"{API_GATEWAY_URL}/get_all_sports")
    sports = response.json()

    for equipe in equipes:
        sport_associe = next((sport for sport in sports if sport['id'] == equipe['id_sport_associe']), None)
        equipe['sport_nom'] = sport_associe['nom'] if sport_associe else "Sport inconnu"

    return render_template('match/ajouter_equipe.html', sports=sports, equipes=equipes)


@match_bp.route('/supprimer_equipe/<int:equipe_id>', methods=['POST'])
def supprimer_equipe(equipe_id):
    response = requests.post(f"{API_GATEWAY_URL}/delete_equipe", json={
        "equipe_id": equipe_id
    })

    if response.status_code == 200:
        flash("Équipe supprimée avec succès.", "success")
    elif response.status_code == 404:
        flash("Équipe non trouvée.", "warning")

    return redirect(url_for('match.ajouter_equipe'))


@match_bp.route('/ajouter_match', methods=['GET', 'POST'])
def ajouter_match():
    if request.method == 'POST':
        data = {
            "id_sport": request.form["id_sport"],
            "id_evenement": request.form["id_evenement"],
            "date": request.form["date"],
            "heure_debut": request.form["heure_debut"],
            "heure_fin": request.form["heure_fin"],
            "id_eq_domicile": request.form["id_eq_domicile"],
            "valeur_cote_domicile": request.form["valeur_cote_domicile"],
            "id_eq_exterieure": request.form["id_eq_exterieure"],
            "valeur_cote_exterieure": request.form["valeur_cote_exterieure"],
            "valeur_cote_match_nul": request.form["valeur_cote_match_nul"],
            "id_bookmaker": session.get("user_id"),
            "est_mis_en_avant": request.form.get("est_mis_en_avant", "off") == "on"
        }

        response = requests.post(f"{API_GATEWAY_URL}/create_match", json=data)

        if response.status_code == 201:
            flash("Match créé avec succès.", "success")
        else:
            flash("Erreur lors de la création du match.", "danger")

    sports = requests.get(f"{API_GATEWAY_URL}/get_all_sports").json()
    evenements = requests.get(f"{API_GATEWAY_URL}/get_all_evenements").json()
    equipes = requests.get(f"{API_GATEWAY_URL}/get_all_equipes").json()
    matchs = requests.get(f"{API_GATEWAY_URL}/get_all_matchs").json()

    return render_template(
        'match/ajouter_match.html',
        sports=sports,
        evenements=evenements,
        equipes=equipes,
        matchs=matchs
    )
