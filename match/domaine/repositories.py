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
        return get_all("sport")

    @staticmethod
    def delete(id):
        return delete_by_id("sport", id)


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
