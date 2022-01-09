"""add last few columns to posts1 table

Revision ID: 457199d78451
Revises: d86265bd725e
Create Date: 2022-01-07 21:28:24.958004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457199d78451'
down_revision = 'd86265bd725e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts1', sa.Column(
        'published', sa.Boolean(), nullable= False, server_default = 'TRUE'
    ),)
    op.add_column('posts1', sa.Column(
        'created_at', sa.TIMESTAMP(timezone='True'), nullable= False, server_default= sa.text("NOW()")
    ),)
    pass


def downgrade():

    op.drop_column('posts1', 'published')
    op.drop_column('posts1', 'created_at')
    pass
