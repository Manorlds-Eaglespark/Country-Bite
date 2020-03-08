"""empty message

Revision ID: 2df9b86f09a3
Revises: 9c29089be11b
Create Date: 2020-04-08 17:56:10.094282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2df9b86f09a3'
down_revision = '9c29089be11b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('shopOwner', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'shopOwner')
    # ### end Alembic commands ###