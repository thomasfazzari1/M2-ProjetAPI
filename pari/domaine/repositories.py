from bdd.connexion import get_db_connection


class ParieurRepository:
    @staticmethod
    def create(parieur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            existe = ParieurRepository.get_by_user_id(parieur.id_utilisateur)
            if existe:
                return None

            cursor.execute(
                """
                INSERT INTO parieur (id_utilisateur, cagnotte)
                VALUES (%s, %s) RETURNING id
                """,
                (parieur.id_utilisateur, parieur.cagnotte)
            )
            parieur_id = cursor.fetchone()[0]
            connection.commit()
            return parieur_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_by_user_id(id_utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT * FROM parieur WHERE id_utilisateur = %s
                """,
                (id_utilisateur,)
            )
            result = cursor.fetchone()
            return result
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_cagnotte_by_user_id(id_utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT cagnotte FROM parieur WHERE id_utilisateur = %s
                """,
                (id_utilisateur,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()
            connection.close()
