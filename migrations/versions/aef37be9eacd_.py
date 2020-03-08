"""empty message

Revision ID: aef37be9eacd
Revises: f83af71bea1f
Create Date: 2020-04-13 12:19:17.524993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aef37be9eacd'
down_revision = 'f83af71bea1f'
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
