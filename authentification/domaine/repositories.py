from bdd.connexion import get_db_connection
from psycopg2.extras import DictCursor


class UtilisateurRepository:
    @staticmethod
    def create(utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO public.utilisateur (pseudo, email, mdp_hash, created_at, updated_at, bookmaker) 
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """,
                (utilisateur.pseudo, utilisateur.email, utilisateur.mdp_hash, utilisateur.created_at,
                 utilisateur.updated_at, utilisateur.bookmaker)
            )
            utilisateur_id = cursor.fetchone()[0]
            connection.commit()
            return utilisateur_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_email(email):
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute("SELECT * FROM public.utilisateur WHERE email = %s", (email,))
            user = cursor.fetchone()
            return dict(user) if user else None
        finally:
            cursor.close()
            connection.close()
