from flask import Blueprint, request, jsonify, make_response
from http import HTTPStatus
from pydantic import ValidationError

from repositories.security_repository import SecurityRepository
from schemas.security_schemas import SecuritySchema

auth_bp = Blueprint("auth", __name__, url_prefix="/login")

@auth_bp.route("/", methods=["POST"])
def login():
    repo = SecurityRepository()
    try:
        data = SecuritySchema(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({"detail": "Dados inválidos"}), HTTPStatus.BAD_REQUEST)

    user = repo.verify_user(data)
    if not user:
        return make_response(jsonify({"detail": "Email ou Senha incorretos."}), HTTPStatus.UNAUTHORIZED)

    access_token = repo.create_access_token({"sub": user.email})
    return make_response(jsonify(access_token=access_token, token_type="Bearer"), HTTPStatus.OK)
