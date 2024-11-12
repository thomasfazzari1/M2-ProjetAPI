from datetime import datetime


class Sport:
    def __init__(self, nom):
        self.nom = nom


class Evenement:
    def __init__(self, nom, id_sport_associe):
        self.nom = nom
        self.id_sport_associe = id_sport_associe


class Equipe:
    def __init__(self, id_sport, nom):
        self.id_sport = id_sport
        self.nom = nom


class Match:
    def __init__(self, id_sport, id_evenement, date, heure_debut, heure_fin,
                 id_eq_domicile, id_cote_eq_domicile, id_eq_exterieure,
                 id_cote_eq_exterieure, id_lieu, created_at=None, updated_at=None, id_bookmaker=None,
                 est_mis_en_avant=False):
        self.id_sport = id_sport
        self.id_evenement = id_evenement
        self.date = date
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.id_eq_domicile = id_eq_domicile
        self.id_cote_eq_domicile = id_cote_eq_domicile
        self.id_eq_exterieure = id_eq_exterieure
        self.id_cote_eq_exterieure = id_cote_eq_exterieure
        self.id_lieu = id_lieu
        self.est_mis_en_avant = est_mis_en_avant
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.created_by = id_bookmaker
        self.updated_by = id_bookmaker


class Cote:
    def __init__(self, id_match, id_equipe, valeur, created_at=None, updated_at=None, created_by=None,
                 updated_by=None):
        self.id_match = id_match
        self.id_equipe = id_equipe
        self.valeur = valeur
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.created_by = created_by
        self.updated_by = updated_by


class Lieu:
    def __init__(self, nom, adresse=None):
        self.nom = nom
        self.adresse = adresse
