"""empty message

Revision ID: 10fa0d809634
Revises: aef37be9eacd
Create Date: 2020-04-13 12:20:35.367243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10fa0d809634'
down_revision = 'aef37be9eacd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ads', 'duration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ads', sa.Column('duration', sa.VARCHAR(length=40), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
