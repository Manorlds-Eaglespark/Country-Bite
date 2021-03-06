"""empty message

Revision ID: becd3f66e1ed
Revises: 2bb3c5b564ac
Create Date: 2020-01-14 22:33:57.343342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'becd3f66e1ed'
down_revision = '2bb3c5b564ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('post', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('time_added', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###
