from flask import Blueprint, request, jsonify, abort, make_response
from http import HTTPStatus
from repositories.users_repository import UsersRepository
from repositories.security_repository import SecurityRepository
from schemas.user_schemas import UserCreate, UserUpdate

users_bp = Blueprint("users", __name__, url_prefix="/users")

def serialize(user):
    data = user.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data

def require_admin(current):
    if not current["is_admin"]:
        abort(make_response(jsonify({"error": "Seu usuário não tem permissão para realizar a ação."}), HTTPStatus.FORBIDDEN))

@users_bp.route("/", methods=["POST"])
def create_user():
    security = SecurityRepository()
    repo = UsersRepository()

    current = security.get_current_user()
    require_admin(current)

    data = UserCreate(**request.get_json())
    user = repo.create(data)
    return jsonify(serialize(user)), HTTPStatus.CREATED

@users_bp.route("/", methods=["GET"])
def read_users():
    security = SecurityRepository()
    repo = UsersRepository()

    current = security.get_current_user()
    require_admin(current)

    users = repo.base_repository.db.query(repo._entity).all()
    return jsonify([serialize(u) for u in users]), HTTPStatus.OK

@users_bp.route("/<int:user_id>", methods=["GET"])
def read_user(user_id):
    security = SecurityRepository()
    repo = UsersRepository()

    current = security.get_current_user()
    if not current["is_admin"] and current["user_id"] != user_id:
        abort(make_response(jsonify({"error": "Acesso proibido."}), HTTPStatus.FORBIDDEN))

    user = repo.find_one(user_id)
    return jsonify(serialize(user)), HTTPStatus.OK

@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    security = SecurityRepository()
    repo = UsersRepository()

    current = security.get_current_user()
    if not current["is_admin"] and current["user_id"] != user_id:
        abort(make_response(jsonify({"error": "Acesso proibido."}), HTTPStatus.FORBIDDEN))

    data = UserUpdate(**request.get_json())
    updated = repo.update(user_id, data)
    return jsonify(serialize(updated)), HTTPStatus.OK

@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    security = SecurityRepository()
    repo = UsersRepository()

    current = security.get_current_user()
    if not current["is_admin"]:
        abort(make_response(jsonify({"error": "Acesso proibido."}), HTTPStatus.FORBIDDEN))
    if current["user_id"] == user_id:
        abort(make_response(jsonify({"error": "Administradores não podem deletar a si mesmos."}), HTTPStatus.FORBIDDEN))

    target = repo.find_one(user_id)
    if target.is_admin:
        abort(make_response(jsonify({"error": "Administradores não podem deletar outros administradores."}), HTTPStatus.FORBIDDEN))

    repo.delete(user_id)
    return "", HTTPStatus.NO_CONTENT
