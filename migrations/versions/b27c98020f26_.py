"""empty message

Revision ID: b27c98020f26
Revises: 136b075b69b6
Create Date: 2020-03-19 05:31:07.465725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b27c98020f26'
down_revision = '136b075b69b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likes', sa.Column('liked_by', sa.Integer(), nullable=True))
    op.add_column('likes', sa.Column('post_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'likes', 'users', ['liked_by'], ['id'])
    op.create_foreign_key(None, 'likes', 'posts', ['post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.drop_column('likes', 'post_id')
    op.drop_column('likes', 'liked_by')
    # ### end Alembic commands ###
