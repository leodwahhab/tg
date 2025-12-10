"""corrigir_tipo_coluna_nome_linha

Revision ID: 236e506eb777
Revises: 6dbbe4e1190d
Create Date: 2025-12-10 11:31:56.255299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '236e506eb777'
down_revision: Union[str, Sequence[str], None] = '523b3eced7b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Alterar o tipo da coluna nome de Integer para String(50)
    op.alter_column('linha', 'nome',
                    existing_type=sa.Integer(),
                    type_=sa.String(length=50),
                    existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Reverter o tipo da coluna nome de String(50) para Integer
    op.alter_column('linha', 'nome',
                    existing_type=sa.String(length=50),
                    type_=sa.Integer(),
                    existing_nullable=False)

