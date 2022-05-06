"""first

Revision ID: 4143a487bc5d
Revises: 867ec4b6dede
Create Date: 2022-05-06 16:10:01.766938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4143a487bc5d'
down_revision = '867ec4b6dede'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('approval_template_step', sa.Column('hash', sa.String(), nullable=True))
    op.drop_index('idx_entity_at', table_name='approval_template_step')
    op.drop_index('ix_approval_template_step_entity_iin', table_name='approval_template_step')
    op.create_index(op.f('ix_approval_template_step_hash'), 'approval_template_step', ['hash'], unique=False)
    op.drop_constraint('approval_template_step_entity_iin_fkey', 'approval_template_step', type_='foreignkey')
    op.drop_column('approval_template_step', 'entity_iin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('approval_template_step', sa.Column('entity_iin', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('approval_template_step_entity_iin_fkey', 'approval_template_step', 'entity', ['entity_iin'], ['iin'], ondelete='CASCADE')
    op.drop_index(op.f('ix_approval_template_step_hash'), table_name='approval_template_step')
    op.create_index('ix_approval_template_step_entity_iin', 'approval_template_step', ['entity_iin'], unique=False)
    op.create_index('idx_entity_at', 'approval_template_step', ['entity_iin', 'approval_template_id'], unique=False)
    op.drop_column('approval_template_step', 'hash')
    # ### end Alembic commands ###