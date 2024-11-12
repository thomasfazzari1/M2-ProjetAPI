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


class EvenementRepository:
    @staticmethod
    def create(evenement):
        return


class EquipeRepository:
    @staticmethod
    def create(equipe):
        return


class MatchRepository:
    @staticmethod
    def create(match):
        return


class LieuRepository:
    @staticmethod
    def create(lieu):
        return


class CoteRepository:
    @staticmethod
    def create(cote):
        return
