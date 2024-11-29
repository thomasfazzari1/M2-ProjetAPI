from bdd.connexion import get_db_connection


class PayeurRepository:
    @staticmethod
    def get_by_user_id(id_utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id FROM public.payeur WHERE id_utilisateur = %s", (id_utilisateur,))
            result = cursor.fetchone()
            return result
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create(id_utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO public.payeur (id_utilisateur) VALUES (%s) RETURNING id",
                (id_utilisateur,)
            )
            payeur_id = cursor.fetchone()[0]
            connection.commit()
            return payeur_id
        finally:
            cursor.close()
            connection.close()


class PaiementRepository:
    @staticmethod
    def create(paiement):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO public.paiement (id_payeur, montant, date, statut)
                VALUES (%s, %s, %s, %s) RETURNING id
                """,
                (paiement.id_payeur, paiement.montant, paiement.date, paiement.statut)
            )

            paiement_id = cursor.fetchone()[0]
            connection.commit()
            return paiement_id
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_by_payeur(id_payeur):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT id, id_payeur, montant, date, statut 
                FROM public.paiement 
                WHERE id_payeur = %s
                ORDER BY date_paiement DESC
                """,
                (id_payeur,)
            )
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            connection.close()
