import os
from flask import Flask
from routes.utilisateur import utilisateur_bp
from routes.match import match_bp

app = Flask(__name__)
app.secret_key = app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(utilisateur_bp)
app.register_blueprint(match_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
