"""empty message

Revision ID: b768ef92e1bf
Revises: 320e4291e882
Create Date: 2024-06-08 02:52:25.189792

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b768ef92e1bf'
down_revision = '320e4291e882'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('s_active', sa.Integer(), nullable=False))
        batch_op.drop_column('active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('s_active')

    # ### end Alembic commands ###