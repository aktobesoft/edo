"""16

Revision ID: b532b04f8188
Revises: d10c2e4fb98c
Create Date: 2022-04-14 12:05:20.552147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b532b04f8188'
down_revision = 'd10c2e4fb98c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase_requisition',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('guid', sa.String(length=36), nullable=False),
    sa.Column('number', sa.String(length=150), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('sum', sa.Integer(), nullable=True),
    sa.Column('counterparty_id', sa.Integer(), nullable=False),
    sa.Column('document_type_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['counterparty_id'], ['counterparty.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['document_type_id'], ['document_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_requisition_guid'), 'purchase_requisition', ['guid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_purchase_requisition_guid'), table_name='purchase_requisition')
    op.drop_table('purchase_requisition')
    # ### end Alembic commands ###