"""autovote

Revision ID: 7dfb0fc8b531
Revises: 457199d78451
Create Date: 2022-01-07 21:53:42.254226

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7dfb0fc8b531'
down_revision = '457199d78451'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user1')
    op.drop_table('posts1')
    op.drop_constraint('posts_users_key', 'users', type_='foreignkey')
    op.drop_column('users', 'user_id')
    op.create_foreign_key(None, 'votes', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.add_column('users', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('posts_users_key', 'users', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_table('posts1',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('published', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user1.id'], name='posts1_users1_fk', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='posts1_pkey')
    )
    op.create_table('user1',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user1_pkey'),
    sa.UniqueConstraint('email', name='user1_email_key')
    )
    # ### end Alembic commands ###
