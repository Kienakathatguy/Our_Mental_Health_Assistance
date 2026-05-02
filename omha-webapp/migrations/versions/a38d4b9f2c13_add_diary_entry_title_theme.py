"""Add title and theme fields to diary_entry

Revision ID: a38d4b9f2c13
Revises: 3917d56c6b02
Create Date: 2026-05-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a38d4b9f2c13'
down_revision = '3917d56c6b02'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('diary_entry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('theme', sa.String(length=50), nullable=True))


def downgrade():
    with op.batch_alter_table('diary_entry', schema=None) as batch_op:
        batch_op.drop_column('theme')
        batch_op.drop_column('title')
