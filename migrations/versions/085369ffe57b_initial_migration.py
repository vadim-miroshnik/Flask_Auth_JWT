"""Initial migration.

Revision ID: 085369ffe57b
Revises: 
Create Date: 2022-09-03 16:08:01.669868

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "085369ffe57b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema auth")
    # ### commands auto generated by Alembic - please adjust! ###
    roles = op.create_table(
        "roles",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("name"),
        schema="auth",
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
        schema="auth",
    )
    op.create_table(
        "history",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["auth.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        schema="auth",
    )
    op.create_table(
        "roles_rights",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("param_name", sa.String(length=128), nullable=True),
        sa.Column("param_value", sa.String(length=128), nullable=True),
        sa.ForeignKeyConstraint(["role"], ["auth.roles.name"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        schema="auth",
    )
    op.create_table(
        "users_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["role"], ["auth.roles.name"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        schema="auth",
    )
    # ### end Alembic commands ###
    # seed data #
    op.bulk_insert(
        roles,
        [
            {"name": "superuser"},
            {"name": "admin"},
            {"name": "regular"},
            {"name": "subscribe"},
            {"name": "guest"},
        ],
    )    


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_roles", schema="auth")
    op.drop_table("roles_rights", schema="auth")
    op.drop_table("history", schema="auth")
    op.drop_table("users", schema="auth")
    op.drop_table("roles", schema="auth")
    # ### end Alembic commands ###
    op.execute("drop schema auth")