from db import db
from werkzeug.security import check_password_hash, generate_password_hash

from models.mixins import IdCreatedUpdatedMixin


class User(IdCreatedUpdatedMixin):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    email = db.Column(db.String(length=120), unique=True, nullable=False)
    password = db.Column(db.String(length=256), nullable=False)

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    def set_password(self, password: str):
        self.password = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.password, password=password)
