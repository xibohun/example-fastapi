"""create  posts table

Revision ID: 6073b6d2c146
Revises: 
Create Date: 2022-01-07 19:25:58.864033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6073b6d2c146'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts1', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    ,sa.Column('title',sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table('posts1')
    pass
