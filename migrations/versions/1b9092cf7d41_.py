"""empty message

Revision ID: 1b9092cf7d41
Revises: 140d2bbaf2e1
Create Date: 2020-04-12 22:29:54.416152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b9092cf7d41'
down_revision = '140d2bbaf2e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ads', sa.Column('country', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ads', 'country')
    # ### end Alembic commands ###