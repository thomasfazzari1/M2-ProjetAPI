from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

authentification_bp = Blueprint('authentification', __name__)


@authentification_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        email = request.form['email']
        mdp = request.form['mdp']

        response = requests.post(f"{API_GATEWAY_URL}/create_user", json={
            "pseudo": pseudo,
            "email": email,
            "mdp": mdp
        })

        if response.status_code == 201:
            flash("Utilisateur créé avec succès.", "success")
            return redirect(url_for('authentification.index'))
        else:
            flash("Erreur lors de la création de l'utilisateur.", "danger")

    return render_template('authentification/register.html')


@authentification_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']

        response = requests.post(f"{API_GATEWAY_URL}/login", json={
            "email": email,
            "mdp": mdp
        })

        if response.status_code == 200:
            user_data = response.json()
            session['user_id'] = user_data['user_id']
            session['pseudo'] = user_data['pseudo']
            session['is_bookmaker'] = user_data['is_bookmaker']
            flash("Connexion réussie.", "success")
            return redirect(url_for('authentification.index'))
        else:
            flash("Erreur lors de la connexion.", "danger")

    return render_template('authentification/login.html')


@authentification_bp.route('/logout')
def logout():
    response = requests.post(f"{API_GATEWAY_URL}/logout")
    if response.status_code == 200:
        session.clear()
    return redirect(url_for('authentification.index'))


@authentification_bp.route('/espace_bookmaker')
def espace_bookmaker():
    response = requests.get(f"{API_GATEWAY_URL}/get_all_sports")
    if response.status_code == 200:
        sports = response.json()
    else:
        flash("Erreur lors du chargement des sports.", "danger")
        sports = []

    return render_template('authentification/espace_bookmaker.html', sports=sports)


@authentification_bp.route('/')
def index():
    if session.get('user_id') and not session.get('is_bookmaker'):
        user_id = session['user_id']
        try:
            response = requests.get(f"{API_GATEWAY_URL}/parieur/{user_id}/cagnotte")
            if response.status_code == 200:
                session['cagnotte'] = response.json().get('cagnotte', 0.00)
            else:
                session['cagnotte'] = 0.00
        except requests.exceptions.RequestException:
            session['cagnotte'] = 0.00
    return render_template('index.html')
