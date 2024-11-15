from bdd.connexion import get_db_connection


# region Sport
class SportRepository:
    @staticmethod
    def create(sport):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO sport (nom) VALUES (%s)",
                (sport.nom,)
            )
            connection.commit()
            sport_id = cursor.lastrowid
            return sport_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_sports():
        return get_all("sport")

    @staticmethod
    def delete(id):
        return delete_by_id("sport", id)


# endregion

# region Evenement
class EvenementRepository:
    @staticmethod
    def create(evenement):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO evenement (nom, id_sport_associe) VALUES (%s, %s)",
                (evenement.nom, evenement.id_sport_associe)
            )
            connection.commit()
            evenement_id = cursor.lastrowid
            return evenement_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_evenements():
        return get_all("evenement")

    @staticmethod
    def delete(id):
        return delete_by_id("evenement", id)


# endregion

# region Equipe
class EquipeRepository:
    @staticmethod
    def create(equipe):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO equipe  (nom, id_sport_associe) VALUES (%s, %s)",
                (equipe.nom, equipe.id_sport_associe,)
            )
            connection.commit()
            equipe_id = cursor.lastrowid
            return equipe_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_equipes():
        return get_all("equipe")

    @staticmethod
    def delete(id):
        return delete_by_id("equipe", id)


# endregion

# region Match
class MatchRepository:
    @staticmethod
    def create(match):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO rencontre (
                    id_sport_associe, id_evenement_associe, date, heure_debut, heure_fin,
                    id_eq_domicile, valeur_cote_eq_domicile, id_eq_exterieure,
                    valeur_cote_eq_exterieure, valeur_cote_match_nul, created_at,
                    updated_at, created_by, updated_by, est_mis_en_avant
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    match.id_sport_associe, match.id_evenement_associe, match.date, match.heure_debut,
                    match.heure_fin, match.id_eq_domicile, match.valeur_cote_eq_domicile,
                    match.id_eq_exterieure, match.valeur_cote_eq_exterieure,
                    match.valeur_cote_match_nul, match.created_at, match.updated_at,
                    match.created_by, match.updated_by, match.est_mis_en_avant
                )
            )
            connection.commit()
            match_id = cursor.lastrowid
            return match_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_matchs():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT r.id, r.id_sport_associe, e.nom AS evenement_nom, eq1.nom AS equipe_domicile, 
                       r.valeur_cote_eq_domicile, eq2.nom AS equipe_exterieure, r.valeur_cote_eq_exterieure, 
                       r.valeur_cote_match_nul, s.nom AS sport_nom, r.est_mis_en_avant, 0 AS nombre_paris
                FROM rencontre r
                JOIN sport s ON r.id_sport_associe = s.id
                JOIN evenement e ON r.id_evenement_associe = e.id
                JOIN equipe eq1 ON r.id_eq_domicile = eq1.id
                JOIN equipe eq2 ON r.id_eq_exterieure = eq2.id
                """
            )
            matchs = cursor.fetchall()

            for match in matchs:
                match['est_mis_en_avant'] = "Oui" if match['est_mis_en_avant'] else "Non"

            return matchs
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(id):
        return delete_by_id("rencontre", id)


# endregion

def get_all(table_name):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def delete_by_id(table_name, id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (id,))
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()
