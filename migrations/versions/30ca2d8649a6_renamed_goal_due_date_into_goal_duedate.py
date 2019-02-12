"""Renamed Goal.due_date into Goal.duedate

Revision ID: 30ca2d8649a6
Revises: 3ca12759cc66
Create Date: 2019-02-12 14:58:29.939919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30ca2d8649a6'
down_revision = '3ca12759cc66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('duedate', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_goal_duedate'), 'goal', ['duedate'], unique=False)
    op.drop_index('ix_goal_due_date', table_name='goal')
    op.drop_column('goal', 'due_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('due_date', sa.DATETIME(), nullable=True))
    op.create_index('ix_goal_due_date', 'goal', ['due_date'], unique=False)
    op.drop_index(op.f('ix_goal_duedate'), table_name='goal')
    op.drop_column('goal', 'duedate')
    # ### end Alembic commands ###