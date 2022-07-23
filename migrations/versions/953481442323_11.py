"""11

Revision ID: 953481442323
Revises: df5e96b08104
Create Date: 2022-07-19 19:32:31.797145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '953481442323'
down_revision = 'df5e96b08104'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('enum_document_type_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('assigned_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assigned_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.ForeignKeyConstraint(['enum_document_type_id'], ['enum_document_type.id'], ),
    sa.ForeignKeyConstraint(['status'], ['enum_task_status_type.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_status_assigned_user_id'), 'task_status', ['assigned_user_id'], unique=False)
    op.create_index(op.f('ix_task_status_author_id'), 'task_status', ['author_id'], unique=False)
    op.create_index(op.f('ix_task_status_document_id'), 'task_status', ['document_id'], unique=False)
    op.create_index(op.f('ix_task_status_entity_iin'), 'task_status', ['entity_iin'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_status_entity_iin'), table_name='task_status')
    op.drop_index(op.f('ix_task_status_document_id'), table_name='task_status')
    op.drop_index(op.f('ix_task_status_author_id'), table_name='task_status')
    op.drop_index(op.f('ix_task_status_assigned_user_id'), table_name='task_status')
    op.drop_table('task_status')
    # ### end Alembic commands ###