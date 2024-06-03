"""empty message

Revision ID: 4bfd0ad074e5
Revises: 55ad01c268b0
Create Date: 2024-05-18 12:40:58.232442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bfd0ad074e5'
down_revision = '55ad01c268b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tel', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_feedback', schema=None) as batch_op:
        batch_op.drop_column('tel')

    # ### end Alembic commands ###
