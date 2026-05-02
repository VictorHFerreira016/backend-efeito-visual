"""add quantidade_minima and data_validade to produtos

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-02 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('produtos', sa.Column('quantidade_minima', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('produtos', sa.Column('data_validade', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('produtos', 'data_validade')
    op.drop_column('produtos', 'quantidade_minima')