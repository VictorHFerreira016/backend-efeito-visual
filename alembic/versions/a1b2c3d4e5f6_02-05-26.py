"""add servico_id to itens_venda

Revision ID: a1b2c3d4e5f6
Revises: 08122cd81486
Create Date: 2026-05-02 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '08122cd81486'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # produto_id passa a ser nullable
    op.alter_column('itens_venda', 'produto_id', nullable=True)

    # adiciona servico_id
    op.add_column('itens_venda',
        sa.Column('servico_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_itens_venda_servico_id',
        'itens_venda', 'servicos',
        ['servico_id'], ['id'],
        ondelete='RESTRICT'
    )


def downgrade() -> None:
    op.drop_constraint('fk_itens_venda_servico_id', 'itens_venda', type_='foreignkey')
    op.drop_column('itens_venda', 'servico_id')
    op.alter_column('itens_venda', 'produto_id', nullable=False)