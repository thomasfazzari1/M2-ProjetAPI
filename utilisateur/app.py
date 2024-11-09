import os
import mysql.connector
from flask import Flask, jsonify, request
from datetime import datetime
import bcrypt

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_disabled=True
    )


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    pseudo = data.get("pseudo")
    email = data.get("email")
    mdp = data.get("mdp")

    if not pseudo or not email or not mdp:
        return jsonify({"error": "Certains champs sont nuls."}), 400

    mdp_hash = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO utilisateur (pseudo, email, mdp_hash, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
            (pseudo, email, mdp_hash, datetime.now(), datetime.now())
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": True, "message": "Utilisateur créé avec succès."}), 201
    except:
        return jsonify({"error": "Erreur lors de la création de l'utilisateur."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
