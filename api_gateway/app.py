from flask import Flask
from routes.utilisateur import utilisateur_bp

app = Flask(__name__)
app.register_blueprint(utilisateur_bp)

@app.route('/')
def default():
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
