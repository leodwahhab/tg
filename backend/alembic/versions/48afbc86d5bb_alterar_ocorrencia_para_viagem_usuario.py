"""alterar_ocorrencia_para_viagem_usuario

Revision ID: 48afbc86d5bb
Revises: f0c499b13e33
Create Date: 2025-12-10 13:39:16.144480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48afbc86d5bb'
down_revision: Union[str, Sequence[str], None] = 'f0c499b13e33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Adicionar novas colunas para referência à viagem_usuario (nullable temporariamente)
    op.add_column('ocorrencia', sa.Column('id_viagem', sa.Integer(), nullable=True))
    op.add_column('ocorrencia', sa.Column('id_usuario_viagem', sa.Integer(), nullable=True))

    # 2. Criar foreign key composta para viagem_usuario
    # Nota: Como viagem_usuario tem PK composta, precisamos das duas colunas
    op.create_foreign_key(
        'fk_ocorrencia_viagem_usuario',
        'ocorrencia',
        'viagem_usuario',
        ['id_viagem', 'id_usuario_viagem'],
        ['id_viagem', 'id_usuario']
    )

    # 3. Remover a constraint de foreign key antiga com usuario
    op.drop_constraint('ocorrencia_id_usuario_fkey', 'ocorrencia', type_='foreignkey')

    # 4. Remover a coluna antiga id_usuario
    op.drop_column('ocorrencia', 'id_usuario')

    # 5. Tornar as novas colunas NOT NULL
    op.alter_column('ocorrencia', 'id_viagem', nullable=False)
    op.alter_column('ocorrencia', 'id_usuario_viagem', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Tornar as colunas nullable temporariamente
    op.alter_column('ocorrencia', 'id_viagem', nullable=True)
    op.alter_column('ocorrencia', 'id_usuario_viagem', nullable=True)

    # 2. Adicionar de volta a coluna id_usuario
    op.add_column('ocorrencia', sa.Column('id_usuario', sa.Integer(), nullable=True))

    # 3. Criar novamente a foreign key com usuario
    op.create_foreign_key(
        'ocorrencia_id_usuario_fkey',
        'ocorrencia',
        'usuario',
        ['id_usuario'],
        ['id']
    )

    # 4. Remover a foreign key composta com viagem_usuario
    op.drop_constraint('fk_ocorrencia_viagem_usuario', 'ocorrencia', type_='foreignkey')

    # 5. Remover as colunas de viagem_usuario
    op.drop_column('ocorrencia', 'id_usuario_viagem')
    op.drop_column('ocorrencia', 'id_viagem')

    # 6. Tornar id_usuario NOT NULL novamente
    op.alter_column('ocorrencia', 'id_usuario', nullable=False)

