from flask import Flask
from application.routes import paiement_bp

app = Flask(__name__)
app.register_blueprint(paiement_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
