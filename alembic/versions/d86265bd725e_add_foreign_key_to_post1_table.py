"""add foreign-key to post1 table

Revision ID: d86265bd725e
Revises: 4dab46070f36
Create Date: 2022-01-07 20:55:49.334770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd86265bd725e'
down_revision = '4dab46070f36'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts1',
                    sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts1_users1_fk', source_table ='posts1', referent_table='user1',
    local_cols = ['owner_id'], remote_cols=['id'], ondelete='CASCADE')




    pass


def downgrade():
    op.drop_constraint('posts1_users1_fk', table_name= 'posts1')
    op.drop_colunm('posts1','owner_id')


    pass
