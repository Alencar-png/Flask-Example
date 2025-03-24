import re
from flask import abort, make_response, jsonify
from repositories.base_repository import BaseRepository
from schemas.user_schemas import UserCreate, UserUpdate
from models.models import User
import bcrypt
from http import HTTPStatus

class UsersRepository:
    def __init__(self):
        self.base_repository = BaseRepository()

    @property
    def _entity(self):
        return User

    def is_valid_email(self, email: str) -> bool:
        pattern = r"(^[\w\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]+$)"
        return re.match(pattern, email) is not None

    def create(self, user_data: UserCreate):
        if not self.is_valid_email(user_data.email):
            abort(make_response(jsonify({"error": "Invalid email."}), HTTPStatus.BAD_REQUEST))

        if self.email_exists(user_data.email):
            abort(make_response(jsonify({"error": "Email already registered."}), HTTPStatus.BAD_REQUEST))

        password_hash = bcrypt.hashpw(
            user_data.password.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=password_hash,
            is_admin=bool(user_data.is_admin)
        )

        try:
            return self.base_repository.create(new_user)
        except Exception:
            abort(make_response(jsonify({"error": "Error creating user."}), HTTPStatus.INTERNAL_SERVER_ERROR))

    def find_one(self, user_id: int):
        user = self.base_repository.find_one(self._entity, user_id)
        if not user:
            abort(make_response(jsonify({"error": "User not found."}), HTTPStatus.NOT_FOUND))
        return user

    def find_all(self):
        return self.base_repository.find_all(self._entity)

    def update(self, user_id: int, user_data: UserUpdate):
        user = self.base_repository.find_one(self._entity, user_id)
        if not user:
            abort(make_response(jsonify({"error": "User not found."}), HTTPStatus.BAD_REQUEST))

        if user_data.email and not self.is_valid_email(user_data.email):
            abort(make_response(jsonify({"error": "Invalid email."}), HTTPStatus.BAD_REQUEST))

        if user_data.email and self.email_exists(user_data.email, user_id):
            abort(make_response(jsonify({"error": "Email already in use."}), HTTPStatus.BAD_REQUEST))

        try:
            updated_user = self.base_repository.update_one(
                self._entity,
                user_id,
                user,
                user_data.model_dump()
            )
            return updated_user
        except Exception:
            abort(make_response(jsonify({"error": "Error updating user."}), HTTPStatus.INTERNAL_SERVER_ERROR))

    def delete(self, user_id: int):
        try:
            deleted = self.base_repository.delete_one(self._entity, user_id)
            return deleted
        except Exception:
            abort(make_response(jsonify({"error": "Error deleting user."}), HTTPStatus.INTERNAL_SERVER_ERROR))

    def email_exists(self, email: str, id: int = 0) -> bool:
        return (
            self.base_repository.db.query(self._entity)
            .filter(self._entity.email == email, self._entity.id != id)
            .first() is not None
        )
