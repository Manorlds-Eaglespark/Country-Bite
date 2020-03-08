"""empty message

Revision ID: 70ace0068d01
Revises: a92d92ba3ea0
Create Date: 2020-03-19 05:07:44.678257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70ace0068d01'
down_revision = 'a92d92ba3ea0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('liked_by', sa.Integer(), nullable=True),
    sa.Column('liked_at', sa.String(length=25), nullable=True),
    sa.ForeignKeyConstraint(['liked_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###
