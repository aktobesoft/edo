"""11

Revision ID: 41a8ca1a181c
Revises: 86ea26c1ca8b
Create Date: 2022-05-03 00:14:52.197254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41a8ca1a181c'
down_revision = '86ea26c1ca8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.drop_constraint('employee_email_key', 'employee', type_='unique')
    op.create_index(op.f('ix_employee_email'), 'employee', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employee_email'), table_name='employee')
    op.create_unique_constraint('employee_email_key', 'employee', ['email'])
    op.drop_index(op.f('ix_approval_template_step_entity_iin'), table_name='approval_template_step')
    op.drop_index(op.f('ix_approval_template_step_employee_id'), table_name='approval_template_step')
    op.drop_index(op.f('ix_approval_template_step_approval_template_id'), table_name='approval_template_step')
    op.drop_index('idx_entity_at', table_name='approval_template_step')
    op.drop_table('approval_template_step')
    # ### end Alembic commands ###
