"""empty message

Revision ID: dffcc843529a
Revises: 56bc8176a06b
Create Date: 2024-04-17 23:01:40.944240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dffcc843529a'
down_revision = '56bc8176a06b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_home_recommend_product',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('product_id', sa.BigInteger(), nullable=True, comment='商品ID'),
    sa.Column('product_name', sa.String(length=64), nullable=True, comment='商品名称'),
    sa.Column('recommend_status', sa.Integer(), nullable=True, comment='推荐状态'),
    sa.Column('sort', sa.Integer(), nullable=True, comment='排序'),
    sa.Column('gmt_create', sa.BigInteger(), nullable=False, comment='创建时间'),
    sa.Column('gmt_modified', sa.BigInteger(), nullable=False, comment='更新时间'),
    sa.Column('create_uid', sa.String(length=64), nullable=False, comment='创建人uid'),
    sa.Column('create_uname', sa.String(length=64), nullable=False, comment='创建人昵称'),
    sa.Column('modified_uid', sa.String(length=64), nullable=False, comment='更新人uid'),
    sa.Column('modified_uname', sa.String(length=64), nullable=False, comment='更新人昵称'),
    sa.Column('enable', sa.SmallInteger(), nullable=False, comment='是否删除:0-未删除;1-删除'),
    sa.Column('merchant_id', sa.Integer(), nullable=True, comment='商户ID'),
    sa.PrimaryKeyConstraint('id'),
    comment='人气推荐商品表'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_home_recommend_product')
    # ### end Alembic commands ###
