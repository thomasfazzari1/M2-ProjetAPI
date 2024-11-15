from datetime import datetime


class Sport:
    def __init__(self, nom):
        self.nom = nom


class Evenement:
    def __init__(self, nom, id_sport_associe):
        self.nom = nom
        self.id_sport_associe = id_sport_associe


class Equipe:
    def __init__(self, nom, id_sport_associe):
        self.nom = nom
        self.id_sport_associe = id_sport_associe


class Match:
    def __init__(self, id_sport_associe, id_evenement_associe, date, heure_debut, heure_fin,
                 id_eq_domicile, valeur_cote_eq_domicile, id_eq_exterieure,
                 valeur_cote_eq_exterieure, valeur_cote_match_nul, created_at=None, updated_at=None, id_bookmaker=None,
                 est_mis_en_avant=False):
        self.id_sport_associe = id_sport_associe
        self.id_evenement_associe = id_evenement_associe
        self.date = date
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.id_eq_domicile = id_eq_domicile
        self.valeur_cote_eq_domicile = valeur_cote_eq_domicile
        self.id_eq_exterieure = id_eq_exterieure
        self.valeur_cote_eq_exterieure = valeur_cote_eq_exterieure
        self.valeur_cote_match_nul = valeur_cote_match_nul
        self.est_mis_en_avant = est_mis_en_avant
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.created_by = id_bookmaker
        self.updated_by = id_bookmaker
