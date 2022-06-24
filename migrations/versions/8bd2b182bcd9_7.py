"""7

Revision ID: 8bd2b182bcd9
Revises: 4e53990e4937
Create Date: 2022-06-25 02:05:41.892011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bd2b182bcd9'
down_revision = '4e53990e4937'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('approval_route_approval_process_id_fkey', 'approval_route', type_='foreignkey')
    op.create_foreign_key(None, 'approval_route', 'approval_process', ['approval_process_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('approval_status_approval_route_id_fkey', 'approval_status', type_='foreignkey')
    op.create_foreign_key(None, 'approval_status', 'approval_route', ['approval_route_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'approval_status', type_='foreignkey')
    op.create_foreign_key('approval_status_approval_route_id_fkey', 'approval_status', 'approval_route', ['approval_route_id'], ['id'])
    op.drop_constraint(None, 'approval_route', type_='foreignkey')
    op.create_foreign_key('approval_route_approval_process_id_fkey', 'approval_route', 'approval_process', ['approval_process_id'], ['id'])
    # ### end Alembic commands ###
