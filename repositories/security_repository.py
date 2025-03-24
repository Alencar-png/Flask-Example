from flask import request, abort, jsonify, make_response
from repositories.base_repository import BaseRepository
from models.models import User
import bcrypt, os
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from schemas.security_schemas import SecuritySchema

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class SecurityRepository:
    def __init__(self):
        self.base_repository = BaseRepository()

    def create_access_token(self, data: dict) -> str:
        payload = data.copy()
        payload.update({
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        })
        return encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_user(self, data: SecuritySchema):
        user = self.base_repository.db.query(User).filter_by(email=data.email).first()
        if user and bcrypt.checkpw(data.password.encode(), user.password.encode()):
            return user
        return None

    def get_current_user(self) -> dict:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            abort(make_response(jsonify({"error": "Acesso não autorizado"}), 401))
        token = auth.split(" ", 1)[1]
        try:
            payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            user = self.base_repository.db.query(User).filter_by(email=email).first()
            if not user:
                abort(make_response(jsonify({"error": "Usuário não encontrado"}), 401))
            return {"user": user, "user_id": user.id, "is_admin": user.is_admin}
        except ExpiredSignatureError:
            abort(make_response(jsonify({"error": "Token expirado"}), 401))
        except InvalidTokenError:
            abort(make_response(jsonify({"error": "Token inválido"}), 401))
