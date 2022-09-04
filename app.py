import os

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade
import click
from api import create_app
from db import db
from models.user import User
from models.role import UserRoles, BaseRoles

app = create_app()
migrate = Migrate(app, db)
jwt = JWTManager(app)


@app.cli.command("create_admin")
@click.argument("email")
@click.argument("password")
def create_admin(email: str, password: str):
    """create new user with admin role"""
    new_user = User(email=email)
    new_user.set_password(password=password)
    db.session.add(new_user)
    db.session.commit()
    UserRoles.assign_user_role(new_user.id, BaseRoles.regular.value)



@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.getenv("FLASK_PORT"))
