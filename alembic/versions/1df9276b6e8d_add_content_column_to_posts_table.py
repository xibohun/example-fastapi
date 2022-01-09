"""add content column to posts table

Revision ID: 1df9276b6e8d
Revises: 6073b6d2c146
Create Date: 2022-01-07 20:19:00.753931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1df9276b6e8d'
down_revision = '6073b6d2c146'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts1',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts1', 'content')
    pass
