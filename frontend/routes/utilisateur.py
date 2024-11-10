from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

utilisateur_bp = Blueprint('utilisateur', __name__)


@utilisateur_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('utilisateur.index'))
        else:
            flash("Erreur lors de la création de l'utilisateur.", "danger")

    return render_template('utilisateur/register.html')


@utilisateur_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('utilisateur.index'))
        else:
            flash("Erreur lors de la connexion.", "danger")

    return render_template('utilisateur/login.html')


@utilisateur_bp.route('/logout')
def logout():
    response = requests.post(f"{API_GATEWAY_URL}/logout")
    if response.status_code == 200:
        session.clear()
    return redirect(url_for('utilisateur.index'))


@utilisateur_bp.route('/')
def index():
    return render_template('index.html')
