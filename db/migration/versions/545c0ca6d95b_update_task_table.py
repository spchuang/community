"""update task table

Revision ID: 545c0ca6d95b
Revises: 9fa4ff6132a
Create Date: 2013-12-23 00:29:55.735389

"""

# revision identifiers, used by Alembic.
revision = '545c0ca6d95b'
down_revision = '9fa4ff6132a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###

    op.add_column('task', sa.Column('status', sa.Integer(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###    
    op.drop_column('task', 'status')

    ### end Alembic commands ###