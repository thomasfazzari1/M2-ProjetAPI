from flask import Blueprint, render_template, request, redirect, url_for, flash
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

@utilisateur_bp.route('/')
def index():
    return render_template('index.html')
