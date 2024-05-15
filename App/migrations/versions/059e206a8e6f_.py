"""empty message

Revision ID: 059e206a8e6f
Revises: 3c8e1edc2487
Create Date: 2024-05-15 23:25:45.161555

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '059e206a8e6f'
down_revision = '3c8e1edc2487'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_feedback',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('category', sa.String(length=60), nullable=False),
    sa.Column('visit_type', sa.String(length=60), nullable=False),
    sa.Column('time_visit', sa.String(length=60), nullable=False),
    sa.Column('date_visit', sa.String(length=20), nullable=False),
    sa.Column('subject', sa.String(length=60), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('tb_feed_back')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_feed_back',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('category', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('visit_type', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('time_visit', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('date_visit', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('subject', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('message', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('tb_feedback')
    # ### end Alembic commands ###