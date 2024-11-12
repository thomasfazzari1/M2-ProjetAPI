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
