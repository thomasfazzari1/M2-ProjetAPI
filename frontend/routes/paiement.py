from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

paiement_bp = Blueprint('paiement', __name__)


@paiement_bp.route('/confirmer_paiement', methods=['GET', 'POST'])
def confirmer_paiement():
    user_id = session.get("user_id")
    montant = session.get("montant_recharge")

    if not user_id:
        flash("Veuillez vous connecter pour effectuer un paiement.", "warning")
        return redirect(url_for('authentification.login'))

    if not montant:
        flash("Aucun montant de recharge sélectionné.", "danger")
        return redirect(url_for('pari.details_cagnotte'))

    payeur_response = requests.get(f"{API_GATEWAY_URL}/paiement/get_payeur/{user_id}")
    if payeur_response.status_code == 404:
        create_response = requests.post(
            f"{API_GATEWAY_URL}/paiement/create_payeur",
            json={"id_utilisateur": user_id}
        )
        if create_response.status_code != 201:
            flash("Erreur lors de la création du profil de payeur.", "danger")
            return redirect(url_for('pari.details_cagnotte'))

    if request.method == 'POST':
        numero_carte = request.form.get("numero_carte")
        expiration = request.form.get("expiration")
        cvc = request.form.get("cvc")

        if not numero_carte or not expiration or not cvc:
            flash("Veuillez remplir tous les champs de la carte bancaire.", "danger")
            return render_template('paiement/confirmer_paiement.html', montant=montant)

        paiement_data = {
            "id_utilisateur": user_id,
            "montant": montant,
            "numero_carte": numero_carte,
            "expiration": expiration,
            "cvc": cvc
        }

        try:
            response = requests.post(f"{API_GATEWAY_URL}/paiement/traiter_paiement_recharge", json=paiement_data)
            if response.status_code == 200:
                cagnotte_response = requests.get(f"{API_GATEWAY_URL}/parieur/{user_id}/cagnotte")
                if cagnotte_response.status_code == 200:
                    session['cagnotte'] = cagnotte_response.json().get("cagnotte", 0.00)
                flash("Paiement effectué avec succès.", "success")
                return redirect(url_for('pari.details_cagnotte'))
            else:
                flash("Erreur lors du paiement. Veuillez réessayer.", "danger")
        except requests.exceptions.RequestException:
            flash("Erreur de communication avec le service de paiement.", "danger")

    return render_template('paiement/confirmer_paiement.html', montant=montant)


@paiement_bp.route('/payer_recharge', methods=['POST'])
def payer_recharge():
    user_id = session.get("user_id")
    if not user_id:
        flash("Veuillez vous connecter pour effectuer un paiement.", "warning")
        return redirect(url_for('authentification.login'))

    montant = request.form.get("montant")

    try:
        montant = float(montant)
        if montant < 10 or montant > 5000:
            flash("Le montant doit être compris entre 10.00 et 5000.00.", "danger")
            return redirect(url_for('pari.details_cagnotte'))

        session['montant_recharge'] = montant
        return redirect(url_for('paiement.confirmer_paiement'))
    except ValueError:
        flash("Veuillez entrer un montant valide.", "danger")
        return redirect(url_for('pari.details_cagnotte'))
