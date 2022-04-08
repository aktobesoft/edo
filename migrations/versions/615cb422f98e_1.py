"""1

Revision ID: 615cb422f98e
Revises: 
Create Date: 2022-03-30 18:25:27.008281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '615cb422f98e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('full_name', sa.String(length=360), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=350), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('entity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
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
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['business_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entity_iin'), 'entity', ['iin'], unique=True)
    op.create_table('сounterparty',
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
    op.create_index(op.f('ix_сounterparty_iin'), 'сounterparty', ['iin'], unique=True)
    op.create_table('employee',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('employee_activity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('last_activity', sa.DateTime(timezone=True), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee_activity')
    op.drop_table('employee')
    op.drop_index(op.f('ix_сounterparty_iin'), table_name='сounterparty')
    op.drop_table('сounterparty')
    op.drop_index(op.f('ix_entity_iin'), table_name='entity')
    op.drop_table('entity')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('notes')
    op.drop_table('document_type')
    op.drop_table('business_type')
    # ### end Alembic commands ###
