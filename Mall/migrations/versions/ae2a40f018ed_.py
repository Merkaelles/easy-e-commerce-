"""empty message

Revision ID: ae2a40f018ed
Revises: b061bf5f461b
Create Date: 2024-04-12 21:31:18.774698

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ae2a40f018ed'
down_revision = 'b061bf5f461b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('status', mysql.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
