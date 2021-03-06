"""4

Revision ID: b77a02b01383
Revises: 4d8ab12d2a3c
Create Date: 2022-07-17 18:17:49.963399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b77a02b01383'
down_revision = '4d8ab12d2a3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('employee_task', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_index(op.f('ix_employee_task_author_id'), 'employee_task', ['author_id'], unique=False)
    op.alter_column('purchase_requisition', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_index(op.f('ix_purchase_requisition_author_id'), 'purchase_requisition', ['author_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_purchase_requisition_author_id'), table_name='purchase_requisition')
    op.alter_column('purchase_requisition', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index(op.f('ix_employee_task_author_id'), table_name='employee_task')
    op.alter_column('employee_task', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
