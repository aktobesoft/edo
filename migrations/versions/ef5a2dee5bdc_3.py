"""3

Revision ID: ef5a2dee5bdc
Revises: 700642bd4504
Create Date: 2022-03-30 19:26:48.252209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef5a2dee5bdc'
down_revision = '700642bd4504'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'document_type', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'document_type', type_='unique')
    # ### end Alembic commands ###