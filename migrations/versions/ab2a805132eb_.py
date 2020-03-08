"""empty message

Revision ID: ab2a805132eb
Revises: 10fa0d809634
Create Date: 2020-04-13 12:20:50.016368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab2a805132eb'
down_revision = '10fa0d809634'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ads', sa.Column('duration', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ads', 'duration')
    # ### end Alembic commands ###