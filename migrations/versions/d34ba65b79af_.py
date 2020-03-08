"""empty message

Revision ID: d34ba65b79af
Revises: e70576135dac
Create Date: 2020-03-07 17:56:01.282224

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd34ba65b79af'
down_revision = 'e70576135dac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('image_delete_hash', sa.String(length=100), nullable=True))
    op.add_column('posts', sa.Column('image_url', sa.String(length=100), nullable=True))
    op.add_column('posts', sa.Column('posted_at', sa.DateTime(), nullable=True))
    op.drop_column('posts', 'image')
    op.drop_column('posts', 'created_on')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('posts', sa.Column('image', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('posts', 'posted_at')
    op.drop_column('posts', 'image_url')
    op.drop_column('posts', 'image_delete_hash')
    # ### end Alembic commands ###