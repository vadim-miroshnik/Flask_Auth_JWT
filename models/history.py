from db import db
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import UUID

from models.mixins import IdCreatedUpdatedMixin


@dataclass
class History(IdCreatedUpdatedMixin):
    __tablename__ = "history"
    __table_args__ = {"schema": "auth"}    
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("auth.users.id"))
    description = db.Column(db.String(length=500), nullable=False)
