from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

pari_bp = Blueprint('pari', __name__)


@pari_bp.route('/details_cagnotte', methods=['GET'])
def details_cagnotte():
    user_id = session.get("user_id")
    if not user_id:
        flash("Veuillez vous connecter pour voir votre cagnotte.", "warning")
        return redirect(url_for('authentification.login'))

    try:
        response = requests.get(f"{API_GATEWAY_URL}/parieur/{user_id}/cagnotte")
        if response.status_code == 200:
            cagnotte = response.json().get("cagnotte", 0.00)
        else:
            cagnotte = 0.00
    except requests.exceptions.RequestException:
        flash("Erreur lors de la récupération de la cagnotte.", "danger")
        cagnotte = 0.00

    return render_template('pari/details_cagnotte.html', cagnotte=cagnotte)
