from datetime import datetime


class Payeur:
    def __init__(self, id_utilisateur=None):
        self.id_utilisateur = id_utilisateur


class Paiement:
    def __init__(self, id_payeur, montant, date, statut):
        self.id_payeur = id_payeur
        self.montant = montant
        self.date = date or datetime.now()
        self.statut = statut or "en attente"
