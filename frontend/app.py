from flask import Flask
from routes.utilisateur import utilisateur_bp

app = Flask(__name__)
app.secret_key = 'TheRealDeal'

app.register_blueprint(utilisateur_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
