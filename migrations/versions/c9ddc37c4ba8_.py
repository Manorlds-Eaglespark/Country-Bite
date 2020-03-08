"""empty message

Revision ID: c9ddc37c4ba8
Revises: 6e4766c472ae
Create Date: 2020-03-25 01:04:39.237982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9ddc37c4ba8'
down_revision = '6e4766c472ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('bookmarks_post_id_fkey', 'bookmarks', type_='foreignkey')
    op.drop_constraint('bookmarks_user_id_fkey', 'bookmarks', type_='foreignkey')
    op.drop_column('bookmarks', 'post_id')
    op.drop_column('bookmarks', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('bookmarks', sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('bookmarks_user_id_fkey', 'bookmarks', 'users', ['user_id'], ['id'])
    op.create_foreign_key('bookmarks_post_id_fkey', 'bookmarks', 'posts', ['post_id'], ['id'])
    # ### end Alembic commands ###