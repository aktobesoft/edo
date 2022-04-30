"""3

Revision ID: 62d49c488844
Revises: 5b7a7eae05f8
Create Date: 2022-04-27 17:41:15.749674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62d49c488844'
down_revision = '5b7a7eae05f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase_requisition_t_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('line_number', sa.Integer(), nullable=False),
    sa.Column('service', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(length=360), nullable=False),
    sa.Column('description_code', sa.String(length=36), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('sum', sa.Float(), nullable=True),
    sa.Column('purchase_requisition_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['purchase_requisition_id'], ['purchase_requisition.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_requisition_t_items_purchase_requisition_id'), 'purchase_requisition_t_items', ['purchase_requisition_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_purchase_requisition_t_items_purchase_requisition_id'), table_name='purchase_requisition_t_items')
    op.drop_table('purchase_requisition_t_items')
    # ### end Alembic commands ###
