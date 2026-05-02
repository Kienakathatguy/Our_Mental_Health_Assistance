"""Add advanced personalization fields to diary_entry

Revision ID: a38d4b9f2c14
Revises: a38d4b9f2c13
Create Date: 2026-05-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a38d4b9f2c14'
down_revision = 'a38d4b9f2c13'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('diary_entry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('font', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('background', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('image', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('stickers', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('diary_entry', schema=None) as batch_op:
        batch_op.drop_column('stickers')
        batch_op.drop_column('image')
        batch_op.drop_column('background')
        batch_op.drop_column('font')
