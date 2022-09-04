import http

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import fields
from models.history import History

from ... import ma


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
        tags:
          - user
        """
        user_id: str = get_jwt_identity()
        page = 1
        per_page = 10
        history = History.query.filter_by(user_id=user_id).paginate(
            page, per_page, error_out=False
        )
        return {"history": history_schema.dump(history.items)}, http.HTTPStatus.OK
