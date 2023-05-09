"""fix: set default value to Post.published

Revision ID: 98b625617eec
Revises: bb22aa6dc040
Create Date: 2023-05-08 04:32:16.870544

"""
import sqlalchemy as sa
from sqlalchemy import func

from alembic import op

# revision identifiers, used by Alembic.
revision = "98b625617eec"
down_revision = "bb22aa6dc040"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "posts",
        "published",
        server_default=func.timezone("UTC", func.current_timestamp()),
    )


def downgrade() -> None:
    pass
