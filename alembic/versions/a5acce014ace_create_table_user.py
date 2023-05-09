"""create table user

Revision ID: a5acce014ace
Revises: f89619ef10d6
Create Date: 2023-01-08 12:21:12.407534

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a5acce014ace"
down_revision = ""
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("password", sa.String(256), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
