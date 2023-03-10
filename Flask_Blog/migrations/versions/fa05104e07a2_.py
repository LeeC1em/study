"""empty message

Revision ID: fa05104e07a2
Revises: 80ebebfc6107
Create Date: 2022-12-17 16:29:53.999333

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fa05104e07a2'
down_revision = '80ebebfc6107'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.alter_column('gender',
               existing_type=mysql.VARCHAR(length=1),
               type_=sa.Enum('male', 'female', name='usergender'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.alter_column('gender',
               existing_type=sa.Enum('male', 'female', name='usergender'),
               type_=mysql.VARCHAR(length=1),
               existing_nullable=True)

    # ### end Alembic commands ###
