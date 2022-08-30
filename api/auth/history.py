import http

from app import ma
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import fields
from models.history import History


class HistorySchema(ma.SQLAlchemyAutoSchema):
    created_at = fields.Function(lambda obj: obj.created_at.strftime("%Y-%m-%d %H:%M"))

    class Meta:
        model = History
        fields = ("description", "created_at")
        load_instance = True


history_schema = HistorySchema(many=True)


class LoginHistory(Resource):
    @jwt_required()
    def get(self) -> tuple[dict[str, str], int]:
        """
        Return list of user's login history
        """
        user_id: str = get_jwt_identity()
        history = History.query.filter_by(user_id=user_id)
        return {"history": history_schema.dump(history)}, http.HTTPStatus.OK
