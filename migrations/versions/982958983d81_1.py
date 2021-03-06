"""1

Revision ID: 982958983d81
Revises: 
Create Date: 2022-07-16 18:31:42.334508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '982958983d81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enum_business_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('full_name', sa.String(length=360), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enum_business_type_name'), 'enum_business_type', ['name'], unique=True)
    op.create_table('enum_task_status_type',
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=360), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('enum_document_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('metadata_name', sa.String(length=150), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('metadata_name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('enum_process_status_type',
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=360), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('enum_route_status_type',
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=360), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('enum_step_type',
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=360), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('counterparty',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('full_name', sa.String(length=360), nullable=True),
    sa.Column('iin', sa.String(length=12), nullable=False),
    sa.Column('address', sa.String(length=350), nullable=True),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('contact', sa.String(length=150), nullable=True),
    sa.Column('type_name', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['type_name'], ['enum_business_type.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_counterparty_iin'), 'counterparty', ['iin'], unique=True)
    op.create_table('entity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('full_name', sa.String(length=360), nullable=True),
    sa.Column('iin', sa.String(length=12), nullable=False),
    sa.Column('address', sa.String(length=350), nullable=True),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('director', sa.String(length=150), nullable=True),
    sa.Column('director_phone', sa.String(length=20), nullable=True),
    sa.Column('administrator', sa.String(length=150), nullable=True),
    sa.Column('administrator_phone', sa.String(length=20), nullable=True),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('type_name', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['type_name'], ['enum_business_type.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entity_iin'), 'entity', ['iin'], unique=True)
    op.create_table('approval_template',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('enum_document_type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.ForeignKeyConstraint(['enum_document_type_id'], ['enum_document_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('index_at_entity_enum_document_type', 'approval_template', ['entity_iin', 'enum_document_type_id'], unique=False)
    op.create_index(op.f('ix_approval_template_entity_iin'), 'approval_template', ['entity_iin'], unique=False)
    op.create_table('employee',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employee_email'), 'employee', ['email'], unique=True)
    op.create_table('approval_process',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('enum_document_type_id', sa.Integer(), nullable=False),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('approval_template_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['approval_template_id'], ['approval_template.id'], ),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.ForeignKeyConstraint(['enum_document_type_id'], ['enum_document_type.id'], ),
    sa.ForeignKeyConstraint(['status'], ['enum_process_status_type.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approval_process_approval_template_id'), 'approval_process', ['approval_template_id'], unique=False)
    op.create_index(op.f('ix_approval_process_document_id'), 'approval_process', ['document_id'], unique=False)
    op.create_index(op.f('ix_approval_process_entity_iin'), 'approval_process', ['entity_iin'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('entity_iin', sa.String(), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_company', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('approval_route',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('enum_document_type_id', sa.Integer(), nullable=False),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('approval_template_id', sa.Integer(), nullable=False),
    sa.Column('approval_process_id', sa.Integer(), nullable=False),
    sa.Column('hash', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['approval_process_id'], ['approval_process.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['approval_template_id'], ['approval_template.id'], ),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.ForeignKeyConstraint(['enum_document_type_id'], ['enum_document_type.id'], ),
    sa.ForeignKeyConstraint(['type'], ['enum_step_type.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ar_entity_document_id', 'approval_route', ['entity_iin', 'document_id'], unique=False)
    op.create_index(op.f('ix_approval_route_approval_process_id'), 'approval_route', ['approval_process_id'], unique=False)
    op.create_index(op.f('ix_approval_route_approval_template_id'), 'approval_route', ['approval_template_id'], unique=False)
    op.create_index(op.f('ix_approval_route_document_id'), 'approval_route', ['document_id'], unique=False)
    op.create_index(op.f('ix_approval_route_entity_iin'), 'approval_route', ['entity_iin'], unique=False)
    op.create_index(op.f('ix_approval_route_hash'), 'approval_route', ['hash'], unique=False)
    op.create_index(op.f('ix_approval_route_user_id'), 'approval_route', ['user_id'], unique=False)
    op.create_table('approval_template_step',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('approval_template_id', sa.Integer(), nullable=False),
    sa.Column('hash', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['approval_template_id'], ['approval_template.id'], ),
    sa.ForeignKeyConstraint(['type'], ['enum_step_type.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approval_template_step_approval_template_id'), 'approval_template_step', ['approval_template_id'], unique=False)
    op.create_index(op.f('ix_approval_template_step_hash'), 'approval_template_step', ['hash'], unique=False)
    op.create_index(op.f('ix_approval_template_step_user_id'), 'approval_template_step', ['user_id'], unique=False)
    op.create_table('employee_task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('guid', sa.String(length=36), nullable=False),
    sa.Column('number', sa.String(length=150), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('enum_document_type_id', sa.Integer(), nullable=False),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.ForeignKeyConstraint(['enum_document_type_id'], ['enum_document_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employee_task_entity_iin'), 'employee_task', ['entity_iin'], unique=False)
    op.create_index(op.f('ix_employee_task_guid'), 'employee_task', ['guid'], unique=False)
    op.create_table('purchase_requisition',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('guid', sa.String(length=36), nullable=False),
    sa.Column('number', sa.String(length=150), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('sum', sa.Float(), nullable=True),
    sa.Column('counterparty_iin', sa.String(), nullable=False),
    sa.Column('enum_document_type_id', sa.Integer(), nullable=False),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['counterparty_iin'], ['counterparty.iin'], ),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.ForeignKeyConstraint(['enum_document_type_id'], ['enum_document_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_requisition_counterparty_iin'), 'purchase_requisition', ['counterparty_iin'], unique=False)
    op.create_index(op.f('ix_purchase_requisition_entity_iin'), 'purchase_requisition', ['entity_iin'], unique=False)
    op.create_index(op.f('ix_purchase_requisition_guid'), 'purchase_requisition', ['guid'], unique=False)
    op.create_table('user_activity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('device_token', sa.String(), nullable=True),
    sa.Column('last_activity', sa.DateTime(timezone=True), nullable=True),
    sa.Column('action', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_activity_user_id'), 'user_activity', ['user_id'], unique=False)
    op.create_table('approval_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('enum_document_type_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('comment', sa.String(length=350), nullable=True),
    sa.Column('entity_iin', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('approval_route_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['approval_route_id'], ['approval_route.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_iin'], ['entity.iin'], ),
    sa.ForeignKeyConstraint(['enum_document_type_id'], ['enum_document_type.id'], ),
    sa.ForeignKeyConstraint(['status'], ['enum_route_status_type.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_as_approval_route_id_user_id', 'approval_status', ['approval_route_id', 'user_id'], unique=False)
    op.create_index(op.f('ix_approval_status_approval_route_id'), 'approval_status', ['approval_route_id'], unique=False)
    op.create_index(op.f('ix_approval_status_document_id'), 'approval_status', ['document_id'], unique=False)
    op.create_index(op.f('ix_approval_status_entity_iin'), 'approval_status', ['entity_iin'], unique=False)
    op.create_index(op.f('ix_approval_status_user_id'), 'approval_status', ['user_id'], unique=False)
    op.create_table('purchase_requisition_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('service', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(length=360), nullable=False),
    sa.Column('description_code', sa.String(length=36), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('sum', sa.Float(), nullable=True),
    sa.Column('hash', sa.String(), nullable=True),
    sa.Column('purchase_requisition_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['purchase_requisition_id'], ['purchase_requisition.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_requisition_items_hash'), 'purchase_requisition_items', ['hash'], unique=False)
    op.create_index(op.f('ix_purchase_requisition_items_purchase_requisition_id'), 'purchase_requisition_items', ['purchase_requisition_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_purchase_requisition_items_purchase_requisition_id'), table_name='purchase_requisition_items')
    op.drop_index(op.f('ix_purchase_requisition_items_hash'), table_name='purchase_requisition_items')
    op.drop_table('purchase_requisition_items')
    op.drop_index(op.f('ix_approval_status_user_id'), table_name='approval_status')
    op.drop_index(op.f('ix_approval_status_entity_iin'), table_name='approval_status')
    op.drop_index(op.f('ix_approval_status_document_id'), table_name='approval_status')
    op.drop_index(op.f('ix_approval_status_approval_route_id'), table_name='approval_status')
    op.drop_index('idx_as_approval_route_id_user_id', table_name='approval_status')
    op.drop_table('approval_status')
    op.drop_index(op.f('ix_user_activity_user_id'), table_name='user_activity')
    op.drop_table('user_activity')
    op.drop_index(op.f('ix_purchase_requisition_guid'), table_name='purchase_requisition')
    op.drop_index(op.f('ix_purchase_requisition_entity_iin'), table_name='purchase_requisition')
    op.drop_index(op.f('ix_purchase_requisition_counterparty_iin'), table_name='purchase_requisition')
    op.drop_table('purchase_requisition')
    op.drop_index(op.f('ix_employee_task_guid'), table_name='employee_task')
    op.drop_index(op.f('ix_employee_task_entity_iin'), table_name='employee_task')
    op.drop_table('employee_task')
    op.drop_index(op.f('ix_approval_template_step_user_id'), table_name='approval_template_step')
    op.drop_index(op.f('ix_approval_template_step_hash'), table_name='approval_template_step')
    op.drop_index(op.f('ix_approval_template_step_approval_template_id'), table_name='approval_template_step')
    op.drop_table('approval_template_step')
    op.drop_index(op.f('ix_approval_route_user_id'), table_name='approval_route')
    op.drop_index(op.f('ix_approval_route_hash'), table_name='approval_route')
    op.drop_index(op.f('ix_approval_route_entity_iin'), table_name='approval_route')
    op.drop_index(op.f('ix_approval_route_document_id'), table_name='approval_route')
    op.drop_index(op.f('ix_approval_route_approval_template_id'), table_name='approval_route')
    op.drop_index(op.f('ix_approval_route_approval_process_id'), table_name='approval_route')
    op.drop_index('idx_ar_entity_document_id', table_name='approval_route')
    op.drop_table('approval_route')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_approval_process_entity_iin'), table_name='approval_process')
    op.drop_index(op.f('ix_approval_process_document_id'), table_name='approval_process')
    op.drop_index(op.f('ix_approval_process_approval_template_id'), table_name='approval_process')
    op.drop_table('approval_process')
    op.drop_index(op.f('ix_employee_email'), table_name='employee')
    op.drop_table('employee')
    op.drop_index(op.f('ix_approval_template_entity_iin'), table_name='approval_template')
    op.drop_index('index_at_entity_enum_document_type', table_name='approval_template')
    op.drop_table('approval_template')
    op.drop_index(op.f('ix_entity_iin'), table_name='entity')
    op.drop_table('entity')
    op.drop_index(op.f('ix_counterparty_iin'), table_name='counterparty')
    op.drop_table('counterparty')
    op.drop_table('notes')
    op.drop_table('enum_step_type')
    op.drop_table('enum_route_status_type')
    op.drop_table('enum_process_status_type')
    op.drop_table('enum_document_type')
    op.drop_table('enum_task_status_type')
    op.drop_index(op.f('ix_enum_business_type_name'), table_name='enum_business_type')
    op.drop_table('enum_business_type')
    # ### end Alembic commands ###
