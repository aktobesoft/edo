"""4

Revision ID: 36659ef5e980
Revises: 62d49c488844
Create Date: 2022-04-27 17:41:46.172530

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36659ef5e980'
down_revision = '62d49c488844'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ct_purchase_requisition_items',
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
    op.create_index(op.f('ix_ct_purchase_requisition_items_purchase_requisition_id'), 'ct_purchase_requisition_items', ['purchase_requisition_id'], unique=False)
    op.drop_index('ix_purchase_requisition_t_items_purchase_requisition_id', table_name='purchase_requisition_t_items')
    op.drop_table('purchase_requisition_t_items')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase_requisition_t_items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('line_number', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('service', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=360), autoincrement=False, nullable=False),
    sa.Column('description_code', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('quantity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('sum', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('purchase_requisition_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['purchase_requisition_id'], ['purchase_requisition.id'], name='purchase_requisition_t_items_purchase_requisition_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='purchase_requisition_t_items_pkey')
    )
    op.create_index('ix_purchase_requisition_t_items_purchase_requisition_id', 'purchase_requisition_t_items', ['purchase_requisition_id'], unique=False)
    op.drop_index(op.f('ix_ct_purchase_requisition_items_purchase_requisition_id'), table_name='ct_purchase_requisition_items')
    op.drop_table('ct_purchase_requisition_items')
    # ### end Alembic commands ###