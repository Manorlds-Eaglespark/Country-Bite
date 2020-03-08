"""empty message

Revision ID: 0965da7d9d6b
Revises: c9ddc37c4ba8
Create Date: 2020-03-25 01:05:02.111051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0965da7d9d6b'
down_revision = 'c9ddc37c4ba8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('post_id', sa.Integer(), nullable=True))
    op.add_column('bookmarks', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bookmarks', 'posts', ['post_id'], ['id'])
    op.create_foreign_key(None, 'bookmarks', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.drop_column('bookmarks', 'user_id')
    op.drop_column('bookmarks', 'post_id')
    # ### end Alembic commands ###
