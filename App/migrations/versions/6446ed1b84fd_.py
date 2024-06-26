"""empty message

Revision ID: 6446ed1b84fd
Revises: d75f4a2fae60
Create Date: 2024-06-03 22:11:28.466470

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6446ed1b84fd'
down_revision = 'd75f4a2fae60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ranting', sa.Integer(), nullable=False))
        batch_op.drop_column('time_visit')
        batch_op.drop_column('category')
        batch_op.drop_column('subject')
        batch_op.drop_column('date_visit')
        batch_op.drop_column('visit_type')

    with op.batch_alter_table('tb_food', schema=None) as batch_op:
        batch_op.alter_column('info',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=200),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_food', schema=None) as batch_op:
        batch_op.alter_column('info',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=255),
               nullable=True)

    with op.batch_alter_table('tb_feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visit_type', mysql.VARCHAR(length=60), nullable=False))
        batch_op.add_column(sa.Column('date_visit', mysql.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('subject', mysql.VARCHAR(length=60), nullable=False))
        batch_op.add_column(sa.Column('category', mysql.VARCHAR(length=60), nullable=False))
        batch_op.add_column(sa.Column('time_visit', mysql.VARCHAR(length=60), nullable=False))
        batch_op.drop_column('ranting')

    # ### end Alembic commands ###
