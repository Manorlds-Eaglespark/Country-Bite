"""empty message

Revision ID: e71ae591f042
Revises: 9d715043ca94
Create Date: 2020-04-10 14:39:17.067561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e71ae591f042'
down_revision = '9d715043ca94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'posted_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('posted_at', sa.VARCHAR(length=25), autoincrement=False, nullable=True))
    # ### end Alembic commands ###