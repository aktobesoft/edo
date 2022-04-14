"""9

Revision ID: 84eaea5f926c
Revises: e4490a76387b
Create Date: 2022-04-09 22:11:09.549046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84eaea5f926c'
down_revision = 'e4490a76387b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('counterparty',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('iin', sa.String(length=12), nullable=False),
    sa.Column('address', sa.String(length=350), nullable=True),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('contact', sa.String(length=150), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['business_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_counterparty_iin'), 'counterparty', ['iin'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_counterparty_iin'), table_name='counterparty')
    op.drop_table('counterparty')
    # ### end Alembic commands ###