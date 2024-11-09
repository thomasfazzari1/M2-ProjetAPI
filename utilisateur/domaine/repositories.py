from bdd.connexion import get_db_connection


class UtilisateurRepository:
    @staticmethod
    def create(utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO utilisateur (pseudo, email, mdp_hash, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                (utilisateur.pseudo, utilisateur.email, utilisateur.mdp_hash, utilisateur.created_at,
                 utilisateur.updated_at)
            )
            connection.commit()
            utilisateur_id = cursor.lastrowid
            return utilisateur_id
        finally:
            cursor.close()
            connection.close()
