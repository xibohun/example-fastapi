"""add user1 table

Revision ID: 4dab46070f36
Revises: 1df9276b6e8d
Create Date: 2022-01-07 20:34:02.724546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dab46070f36'
down_revision = '1df9276b6e8d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user1',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                    server_default = sa.text('now()'), nullable= False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
        

    
    pass


def downgrade():
    op.drop_table('user1')
    pass
