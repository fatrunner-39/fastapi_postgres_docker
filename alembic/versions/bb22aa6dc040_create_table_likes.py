"""create table likes

Revision ID: bb22aa6dc040
Revises: 6752ceeb1767
Create Date: 2023-01-09 10:08:04.623352

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'bb22aa6dc040'
down_revision = '6752ceeb1767'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'likes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer()),
        sa.ForeignKeyConstraint(('user_id',), ['users.id'], ondelete='CASCADE'),
        sa.Column('post_id', sa.Integer()),
        sa.ForeignKeyConstraint(('post_id',), ['posts.id'], ondelete='CASCADE'),
        sa.Column('is_like', sa.Boolean, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('likes')
