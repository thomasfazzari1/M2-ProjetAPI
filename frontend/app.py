from flask import Flask
import os
from routes.authentification import authentification_bp
from routes.match import match_bp
from routes.pari import pari_bp

app = Flask(__name__, static_folder='frontend/static')
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(authentification_bp)
app.register_blueprint(match_bp)
app.register_blueprint(pari_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
