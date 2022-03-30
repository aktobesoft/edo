"""5

Revision ID: 64703694f33b
Revises: e4c0b34feb37
Create Date: 2022-03-28 16:22:42.894897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64703694f33b'
down_revision = 'e4c0b34feb37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notes')
    # ### end Alembic commands ###
