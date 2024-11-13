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

    return render_template('utilisateur/bookmaker/ajouter_sport.html', sports=sports)


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

    return render_template('utilisateur/bookmaker/ajouter_evenement.html', sports=sports, evenements=evenements)


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

    return render_template('utilisateur/bookmaker/ajouter_equipe.html', sports=sports, equipes=equipes)


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
