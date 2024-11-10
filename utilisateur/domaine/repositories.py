# repositories.py
from bdd.connexion import get_db_connection


class UtilisateurRepository:
    @staticmethod
    def create(utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO utilisateur (pseudo, email, mdp_hash, created_at, updated_at, bookmaker) VALUES (%s, %s, %s, %s, %s, %s)",
                (utilisateur.pseudo, utilisateur.email, utilisateur.mdp_hash, utilisateur.created_at,
                 utilisateur.updated_at, utilisateur.bookmaker)
            )
            connection.commit()
            utilisateur_id = cursor.lastrowid
            return utilisateur_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_email(email):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user if user else None
        finally:
            cursor.close()
            connection.close()
