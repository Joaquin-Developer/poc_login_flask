from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token #, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from models import User, db


auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


def fake_login(user: str, passw: str) -> bool:
    return user == "jp" and passw == "123"


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # user = User.query.filter_by(email=email).first()
    # if not user or not bcrypt.check_password_hash(user.password_hash, password):
    #     return jsonify({"msg": "Invalid credentials"}), 401
    if not fake_login(email, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # access_token = create_access_token(identity=user.id)
    access_token = create_access_token(identity="123")

    return jsonify(access_token=access_token), 200
