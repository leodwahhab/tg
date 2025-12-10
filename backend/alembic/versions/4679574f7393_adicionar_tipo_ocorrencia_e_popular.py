"""adicionar_tipo_ocorrencia_e_popular

Revision ID: 4679574f7393
Revises: 48afbc86d5bb
Create Date: 2025-12-10 14:33:41.646516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4679574f7393'
down_revision: Union[str, Sequence[str], None] = '48afbc86d5bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Criar tabela tipo_ocorrencia
    op.create_table(
        'tipo_ocorrencia',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome')
    )

    # 2. Definir tabela temporária para inserção
    tipo_ocorrencia_table = sa.table(
        'tipo_ocorrencia',
        sa.column('id', sa.Integer),
        sa.column('nome', sa.String),
        sa.column('descricao', sa.String)
    )

    # 3. Popular tabela tipo_ocorrencia com os tipos de ocorrências
    tipos_ocorrencias = [
        {'id': 1, 'nome': 'Lotação Excessiva', 'descricao': 'Vagão com superlotação, dificultando a movimentação dos passageiros'},
        {'id': 2, 'nome': 'Ar-Condicionado com Defeito', 'descricao': 'Sistema de ar-condicionado não funcionando ou com temperatura inadequada'},
        {'id': 3, 'nome': 'Barulho Excessivo', 'descricao': 'Ruídos altos provenientes de equipamentos ou passageiros'},
        {'id': 4, 'nome': 'Vendedores Ambulantes', 'descricao': 'Presença de vendedores não autorizados no interior do vagão'},
        {'id': 5, 'nome': 'Vazamento de Água', 'descricao': 'Vazamento de água ou líquidos no vagão'},
        {'id': 6, 'nome': 'Iluminação Deficiente', 'descricao': 'Lâmpadas queimadas ou iluminação inadequada no vagão'},
        {'id': 7, 'nome': 'Porta com Defeito', 'descricao': 'Portas não fecham ou abrem corretamente'},
        {'id': 8, 'nome': 'Assento Danificado', 'descricao': 'Bancos quebrados, rasgados ou com defeito'},
        {'id': 9, 'nome': 'Sujeira/Falta de Limpeza', 'descricao': 'Vagão sujo ou com lixo acumulado'},
        {'id': 10, 'nome': 'Mau Cheiro', 'descricao': 'Odores desagradáveis no interior do vagão'},
        {'id': 11, 'nome': 'Mendicância', 'descricao': 'Presença de pessoas pedindo esmolas de forma insistente'},
        {'id': 12, 'nome': 'Vandalismo', 'descricao': 'Danos intencionais ao patrimônio do vagão (pichações, quebra de equipamentos)'},
        {'id': 13, 'nome': 'Comportamento Inadequado', 'descricao': 'Passageiros com comportamento impróprio ou ofensivo'},
        {'id': 14, 'nome': 'Som Alto', 'descricao': 'Uso de aparelhos sonoros em volume alto sem fones de ouvido'},
        {'id': 15, 'nome': 'Fumaça/Cigarro', 'descricao': 'Pessoas fumando dentro do vagão'},
        {'id': 16, 'nome': 'Bebida Alcoólica', 'descricao': 'Consumo de bebidas alcoólicas no interior do vagão'},
        {'id': 17, 'nome': 'Briga/Confusão', 'descricao': 'Alteração ou conflito entre passageiros'},
        {'id': 18, 'nome': 'Emergência Médica', 'descricao': 'Passageiro necessitando de atendimento médico'},
        {'id': 19, 'nome': 'Aviso de Emergência Acionado', 'descricao': 'Botão de emergência acionado indevidamente'},
        {'id': 20, 'nome': 'Outros', 'descricao': 'Outras situações não especificadas acima'}
    ]

    op.bulk_insert(tipo_ocorrencia_table, tipos_ocorrencias)

    # 4. Adicionar nova coluna id_tipo na tabela ocorrencia (nullable temporariamente)
    op.add_column('ocorrencia', sa.Column('id_tipo', sa.Integer(), nullable=True))

    # 5. Criar foreign key para tipo_ocorrencia
    op.create_foreign_key(
        'fk_ocorrencia_tipo_ocorrencia',
        'ocorrencia',
        'tipo_ocorrencia',
        ['id_tipo'],
        ['id']
    )

    # 6. Remover a coluna antiga 'tipo' (string)
    op.drop_column('ocorrencia', 'tipo')

    # 7. Tornar id_tipo NOT NULL
    op.alter_column('ocorrencia', 'id_tipo', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Tornar id_tipo nullable temporariamente
    op.alter_column('ocorrencia', 'id_tipo', nullable=True)

    # 2. Adicionar de volta a coluna 'tipo' como string
    op.add_column('ocorrencia', sa.Column('tipo', sa.String(length=50), nullable=True))

    # 3. Remover foreign key
    op.drop_constraint('fk_ocorrencia_tipo_ocorrencia', 'ocorrencia', type_='foreignkey')

    # 4. Remover coluna id_tipo
    op.drop_column('ocorrencia', 'id_tipo')

    # 5. Tornar coluna tipo NOT NULL
    op.alter_column('ocorrencia', 'tipo', nullable=False)

    # 6. Deletar tabela tipo_ocorrencia
    op.drop_table('tipo_ocorrencia')
