"""create table posts

Revision ID: 6752ceeb1767
Revises: a5acce014ace
Create Date: 2023-01-09 01:06:03.055436

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '6752ceeb1767'
down_revision = 'a5acce014ace'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(('creator_id',), ['users.id'], ondelete='CASCADE'),
        sa.Column('published', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('posts')
