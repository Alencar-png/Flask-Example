from abc import ABC, abstractmethod
from flask import g, current_app
from sqlalchemy.orm import Session, joinedload
from config.database import SessionLocal

def get_db() -> Session:
    """
    Retorna a sessão do SQLAlchemy armazenada em flask.g — criando uma nova se necessário.
    """
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

def close_db(e=None):
    """
    Fecha a sessão ao final de cada request.
    """
    db = g.pop('db', None)
    if db:
        db.close()

class CRUDBase(ABC):
    @property
    @abstractmethod
    def _entity(self):
        ...

    @abstractmethod
    def create(self, item):
        ...

    @abstractmethod
    def find_one(self, item_id, relations=None):
        ...

    @abstractmethod
    def find_all(self, relations=None):
        ...

    @abstractmethod
    def update(self, item_id, current_object, item):
        ...

    @abstractmethod
    def delete(self, item_id):
        ...

class BaseRepository:
    def __init__(self, db: Session = None):
        self.db = db or get_db()

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def find_one(self, entity, item_id: int, relations: list[str] = None):
        opts = [joinedload(getattr(entity, rel)) for rel in relations] if relations else []
        return self.db.query(entity).options(*opts).filter_by(id=item_id).first()

    def find_all(self, entity, relations: list[str] = None):
        opts = [joinedload(getattr(entity, rel)) for rel in relations] if relations else []
        return self.db.query(entity).options(*opts).all()

    def update_one(self, entity, item_id: int, current_object, item):
        try:
            for key, value in item.items():
                setattr(current_object, key, value)
            self.db.commit()
            return self.db.query(entity).get(item_id)
        except Exception:
            self.db.rollback()
            raise

    def delete_one(self, entity, item_id: int):
        try:
            obj = self.db.query(entity).filter_by(id=item_id).first()
            if obj:
                self.db.delete(obj)
                self.db.commit()
        except Exception:
            self.db.rollback()
            raise
