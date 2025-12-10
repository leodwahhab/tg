"""adicionar_coluna_codigo_estacao

Revision ID: f0c499b13e33
Revises: 6dbbe4e1190d
Create Date: 2025-12-10 12:58:36.837501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0c499b13e33'
down_revision: Union[str, Sequence[str], None] = '6dbbe4e1190d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Adicionar coluna codigo (nullable temporariamente)
    op.add_column('estacao', sa.Column('codigo', sa.String(length=3), nullable=True))

    # 2. Mapear nome -> código das estações
    estacoes_codigo = {
        "Júlio Prestes": "JPR",
        "Palmeiras - Barra Funda": "BFU",
        "Lapa": "LAB",
        "Domingos de Moraes": "DMO",
        "Imperatriz Leopoldina": "ILE",
        "Presidente Altino": "PAL",
        "Osasco": "OSA",
        "Comandante Sampaio": "CSA",
        "Quitaúna": "QTU",
        "General Miguel Costa": "GMC",
        "Carapicuíba": "CPB",
        "Santa Terezinha": "STE",
        "Antonio João": "AJO",
        "Barueri": "BRU",
        "Jardim Belval": "JBE",
        "Jardim Silveira": "JSI",
        "Jandira": "JDI",
        "Sagrado Coração": "SCO",
        "Engenheiro Cardoso": "ECD",
        "Itapevi": "IPV",
        "Santa Rita": "SRT",
        "Ambuitá": "AMB",
        "Amador Bueno": "ABU",
        "Varginha": "VAG",
        "Bruno Covas - Mendes - Vila Natal": "MVN",
        "Grajaú": "GRA",
        "Primavera - Interlagos": "INT",
        "Autódromo": "AUT",
        "Jurubatuba - Senac": "JUR",
        "Socorro": "SOC",
        "Santo Amaro": "SAM",
        "Granja Julieta": "GJT",
        "Morumbi - Claro": "MRB",
        "Berrini": "BRR",
        "Vila Olímpia": "VOL",
        "Cidade Jardim": "CJD",
        "Hebraica - Rebouças": "HBR",
        "Pinheiros": "PIN",
        "Cidade Universitária": "USP",
        "Villa Lobos - Jaguaré": "JAG",
        "Ceasa": "CEA",
        "João Dias": "JOD"
    }

    # 3. Atualizar códigos das estações existentes
    for nome, codigo in estacoes_codigo.items():
        op.execute(f"UPDATE estacao SET codigo = '{codigo}' WHERE nome = '{nome}'")

    # 4. Tornar a coluna NOT NULL após popular os dados
    op.alter_column('estacao', 'codigo', nullable=False)

    # 5. Adicionar índice único na coluna codigo para buscas rápidas
    op.create_index('ix_estacao_codigo', 'estacao', ['codigo'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Remover índice e coluna
    op.drop_index('ix_estacao_codigo', table_name='estacao')
    op.drop_column('estacao', 'codigo')

