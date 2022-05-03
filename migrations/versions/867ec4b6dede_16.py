"""16

Revision ID: 867ec4b6dede
Revises: 1513bea961e1
Create Date: 2022-05-03 22:50:01.387891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867ec4b6dede'
down_revision = '1513bea961e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('approval_process',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('document_type_id', sa.Integer(), nullable=False),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.Column('approval_template_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('signed', 'rejected', 'canceled', 'in_process', 'draft', name='status_type'), nullable=True),
    sa.ForeignKeyConstraint(['approval_template_id'], ['approval_template.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['document_type_id'], ['document_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approval_process_approval_template_id'), 'approval_process', ['approval_template_id'], unique=False)
    op.create_index(op.f('ix_approval_process_document_id'), 'approval_process', ['document_id'], unique=False)
    op.create_index(op.f('ix_approval_process_entity_iin'), 'approval_process', ['entity_iin'], unique=False)
    op.create_index(op.f('ix_approval_process_status'), 'approval_process', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_approval_process_status'), table_name='approval_process')
    op.drop_index(op.f('ix_approval_process_entity_iin'), table_name='approval_process')
    op.drop_index(op.f('ix_approval_process_document_id'), table_name='approval_process')
    op.drop_index(op.f('ix_approval_process_approval_template_id'), table_name='approval_process')
    op.drop_table('approval_process')
    # ### end Alembic commands ###
