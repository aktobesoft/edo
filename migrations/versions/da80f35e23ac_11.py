"""11

Revision ID: da80f35e23ac
Revises: 41a8ca1a181c
Create Date: 2022-05-03 00:28:57.019148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da80f35e23ac'
down_revision = '41a8ca1a181c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('approval_template',
    sa.Column('id', sa.Integer(), autoincrement = True, nullable = False),
    sa.Column('document_type_id', sa.Integer(), nullable = False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('entity_iin', sa.String(), nullable = False),
    sa.ForeignKeyConstraint(['document_type_id'], ['document_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_approval_template_entity_iin'), 'approval_template', ['entity_iin'], unique=False)
    op.create_table('approval_template_step',
    sa.Column('id', sa.Integer(), autoincrement = True, nullable = False),
    sa.Column('level', sa.Integer(), nullable = False),
    sa.Column('type', sa.Enum('line', 'paralel', name='steptype'), nullable=True),
    sa.Column('entity_iin', sa.String(), nullable = False),
    sa.Column('employee_id', sa.Integer(), nullable = False),
    sa.Column('approval_template_id', sa.Integer(), nullable = False),
    sa.ForeignKeyConstraint(['approval_template_id'], ['approval_template.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_entity_at', 'approval_template_step', ['entity_iin', 'approval_template_id'], unique=False)
    op.create_index(op.f('ix_approval_template_step_approval_template_id'), 'approval_template_step', ['approval_template_id'], unique=False)
    op.create_index(op.f('ix_approval_template_step_employee_id'), 'approval_template_step', ['employee_id'], unique=False)
    op.create_index(op.f('ix_approval_template_step_entity_iin'), 'approval_template_step', ['entity_iin'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_approval_template_step_entity_iin'), table_name='approval_template_step')
    op.drop_index(op.f('ix_approval_template_step_employee_id'), table_name='approval_template_step')
    op.drop_index(op.f('ix_approval_template_step_approval_template_id'), table_name='approval_template_step')
    op.drop_index('idx_entity_at', table_name='approval_template_step')
    op.drop_table('approval_template_step')
    op.drop_index(op.f('ix_approval_template_entity_iin'), table_name='approval_template')
    op.drop_table('approval_template')
    # ### end Alembic commands ###
