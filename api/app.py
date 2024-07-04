import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from models import db
from config import config
from auth import auth_bp


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config.from_object(config[os.getenv("FLASK_CONFIG") or "default"])

jwt = JWTManager(app)
db.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/auth")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
