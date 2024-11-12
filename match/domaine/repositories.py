from bdd.connexion import get_db_connection


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
        connection = get_db_connection()
        cursor = connection.cursor(
            dictionary=True)
        try:
            cursor.execute("SELECT * FROM sport")
            sports = cursor.fetchall()
            return sports
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(id):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM sport WHERE id = %s", (id,))
            connection.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            connection.close()


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
        connection = get_db_connection()
        cursor = connection.cursor(
            dictionary=True)
        try:
            cursor.execute("SELECT * FROM evenement")
            evenements = cursor.fetchall()
            return evenements
        finally:
            cursor.close()
            connection.close()


class EquipeRepository:
    @staticmethod
    def create(equipe):
        return


class MatchRepository:
    @staticmethod
    def create(match):
        return
