from bdd.connexion import get_db_connection
from psycopg2.extras import DictCursor


# region Sport
class SportRepository:
    @staticmethod
    def create(sport):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO public.sport (nom) VALUES (%s) RETURNING id",
                (sport.nom,)
            )
            sport_id = cursor.fetchone()[0]
            connection.commit()
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

    @staticmethod
    def get_by_name(nom):
        return get_by_field("sport", "nom", nom)

    @staticmethod
    def get_by_id(id):
        return get_by_field("sport", "id", id)


# endregion

# region Evenement
class EvenementRepository:
    @staticmethod
    def create(evenement):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO public.evenement (nom, id_sport_associe) VALUES (%s, %s) RETURNING id",
                (evenement.nom, evenement.id_sport_associe)
            )
            evenement_id = cursor.fetchone()[0]
            connection.commit()
            return evenement_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_evenements():
        return get_all("evenement")

    @staticmethod
    def get_by_id(id):
        return get_by_field("evenement", "id", id)

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
                "INSERT INTO public.equipe (nom, id_sport_associe) VALUES (%s, %s) RETURNING id",
                (equipe.nom, equipe.id_sport_associe,)
            )
            equipe_id = cursor.fetchone()[0]
            connection.commit()
            return equipe_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_equipes():
        return get_all("equipe")

    @staticmethod
    def get_by_name(nom):
        return get_by_field("equipe", "nom", nom)

    @staticmethod
    def get_by_id(id):
        return get_by_field("equipe", "id", id)

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
                INSERT INTO public.rencontre (
                    id_sport_associe, id_evenement_associe, date, heure_debut, heure_fin,
                    id_eq_domicile, valeur_cote_eq_domicile, id_eq_exterieure,
                    valeur_cote_exterieure, valeur_cote_match_nul, created_at,
                    updated_at, created_by, updated_by, est_mis_en_avant
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """,
                (
                    match.id_sport_associe, match.id_evenement_associe, match.date, match.heure_debut,
                    match.heure_fin, match.id_eq_domicile, match.valeur_cote_eq_domicile,
                    match.id_eq_exterieure, match.valeur_cote_exterieure,
                    match.valeur_cote_match_nul, match.created_at, match.updated_at,
                    match.created_by, match.updated_by, match.est_mis_en_avant
                )
            )
            match_id = cursor.fetchone()[0]
            connection.commit()
            return match_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_matchs():
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT r.id, r.id_sport_associe, e.nom AS evenement_nom, eq1.nom AS equipe_domicile, 
                       r.valeur_cote_eq_domicile, eq2.nom AS equipe_exterieure, r.valeur_cote_exterieure, 
                       r.valeur_cote_match_nul, s.nom AS sport_nom, r.est_mis_en_avant, 0 AS nombre_paris
                FROM public.rencontre r
                JOIN public.sport s ON r.id_sport_associe = s.id
                JOIN public.evenement e ON r.id_evenement_associe = e.id
                JOIN public.equipe eq1 ON r.id_eq_domicile = eq1.id
                JOIN public.equipe eq2 ON r.id_eq_exterieure = eq2.id
                """
            )
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            matchs = [dict(zip(colnames, row)) for row in rows]

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

# region Bookmaker
class BookmakerRepository:
    @staticmethod
    def create(bookmaker):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            existe = BookmakerRepository.get_by_user_id(bookmaker.id_utilisateur)
            if existe:
                return None

            cursor.execute(
                """
                INSERT INTO public.bookmaker (id_utilisateur)
                VALUES (%s) RETURNING id
                """,
                (bookmaker.id_utilisateur,)
            )

            bookmaker_id = cursor.fetchone()[0]
            connection.commit()
            return bookmaker_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_by_user_id(user_id):
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute("SELECT * FROM public.bookmaker WHERE id_utilisateur = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_by_id(id):
        return get_by_field("bookmaker", "id", id)


# endregion

def get_all(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM public.{table_name}")
        rows = cursor.fetchall()

        colnames = [desc[0] for desc in cursor.description]
        results = [dict(zip(colnames, row)) for row in rows]

        return results
    finally:
        cursor.close()
        connection.close()


def delete_by_id(table_name, id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(f"DELETE FROM public.{table_name} WHERE id = %s", (id,))
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()


def get_by_field(table_name, field_name, field_value):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = f"SELECT * FROM public.{table_name} WHERE {field_name} = %s"
        cursor.execute(query, (field_value,))
        row = cursor.fetchone()
        if row:
            colnames = [desc[0] for desc in cursor.description]
            return dict(zip(colnames, row))
        return None
    finally:
        cursor.close()
        connection.close()
