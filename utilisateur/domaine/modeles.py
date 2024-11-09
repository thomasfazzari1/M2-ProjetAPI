from datetime import datetime


class Utilisateur:
    def __init__(self, pseudo, email, mdp_hash, created_at=None, updated_at=None):
        self.pseudo = pseudo
        self.email = email
        self.mdp_hash = mdp_hash
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
