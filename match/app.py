from flask import Flask
from application.routes import match_bp

app = Flask(__name__)
app.register_blueprint(match_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
