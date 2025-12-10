"""popular_linhas_e_estacoes

Revision ID: 6dbbe4e1190d
Revises: 523b3eced7b3
Create Date: 2025-12-10 11:15:48.552474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dbbe4e1190d'
down_revision: Union[str, Sequence[str], None] = '236e506eb777'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Definir tabelas temporárias
    linha_table = sa.table(
        'linha',
        sa.column('id', sa.Integer),
        sa.column('nome', sa.String),
        sa.column('numero', sa.Integer),
        sa.column('cor_hex', sa.String)
    )

    estacao_table = sa.table(
        'estacao',
        sa.column('id', sa.Integer),
        sa.column('nome', sa.String),
        sa.column('latitude', sa.Double),
        sa.column('longitude', sa.Double)
    )

    linha_estacao_table = sa.table(
        'linha_estacao',
        sa.column('id_linha', sa.Integer),
        sa.column('id_estacao', sa.Integer),
        sa.column('ordem', sa.Integer)
    )

    # Dicionário de estações (código -> nome)
    estacoes_dict = {
        "VAG": "Varginha",
        "MVN": "Bruno Covas - Mendes - Vila Natal",
        "GRA": "Grajaú",
        "INT": "Primavera - Interlagos",
        "AUT": "Autódromo",
        "JUR": "Jurubatuba - Senac",
        "SOC": "Socorro",
        "SAM": "Santo Amaro",
        "GJT": "Granja Julieta",
        "MRB": "Morumbi - Claro",
        "BRR": "Berrini",
        "VOL": "Vila Olímpia",
        "CJD": "Cidade Jardim",
        "HBR": "Hebraica - Rebouças",
        "PIN": "Pinheiros",
        "USP": "Cidade Universitária",
        "JAG": "Villa Lobos - Jaguaré",
        "CEA": "Ceasa",
        "JOD": "João Dias",
        "PAL": "Presidente Altino",
        "OSA": "Osasco",
        "JPR": "Júlio Prestes",
        "BFU": "Palmeiras - Barra Funda",
        "LAB": "Lapa",
        "DMO": "Domingos de Moraes",
        "ILE": "Imperatriz Leopoldina",
        "CSA": "Comandante Sampaio",
        "QTU": "Quitaúna",
        "GMC": "General Miguel Costa",
        "CPB": "Carapicuíba",
        "STE": "Santa Terezinha",
        "AJO": "Antonio João",
        "BRU": "Barueri",
        "JBE": "Jardim Belval",
        "JSI": "Jardim Silveira",
        "JDI": "Jandira",
        "SCO": "Sagrado Coração",
        "ECD": "Engenheiro Cardoso",
        "IPV": "Itapevi",
        "SRT": "Santa Rita",
        "AMB": "Ambuitá",
        "ABU": "Amador Bueno"
    }

    # Linhas e suas estações em ordem
    linhas_dict = {
        "L8": ["JPR", "BFU", "LAB", "DMO", "ILE", "PAL", "OSA", "CSA",
               "QTU", "GMC", "CPB", "STE", "AJO", "BRU", "JBE", "JSI",
               "JDI", "SCO", "ECD", "IPV", "SRT", "AMB", "ABU"],
        "L9": ["VAG", "MVN", "GRA", "INT", "AUT", "JUR", "SOC", "SAM",
               "GJT", "MRB", "BRR", "VOL", "CJD", "HBR", "PIN", "USP",
               "JAG", "CEA", "JOD", "PAL", "OSA"]
    }

    # 1. Inserir Linhas (8 - Diamante e 9 - Esmeralda)
    op.bulk_insert(linha_table, [
        {'id': 8, 'nome': 'Diamante', 'numero': 8, 'cor_hex': '97005D'},
        {'id': 9, 'nome': 'Esmeralda', 'numero': 9, 'cor_hex': '00A88E'}
    ])

    # 2. Criar mapeamento código -> ID para estações
    # Coletar todas as estações únicas das duas linhas
    estacoes_codes = []
    for linha_codes in linhas_dict.values():
        for code in linha_codes:
            if code not in estacoes_codes:
                estacoes_codes.append(code)

    # 3. Inserir estações com IDs sequenciais
    estacoes_data = []
    codigo_to_id = {}
    for idx, code in enumerate(estacoes_codes, start=1):
        codigo_to_id[code] = idx
        estacoes_data.append({
            'id': idx,
            'nome': estacoes_dict[code],
            'latitude': 0.0,  # Valores padrão (podem ser atualizados depois)
            'longitude': 0.0
        })

    op.bulk_insert(estacao_table, estacoes_data)

    # 4. Inserir relacionamentos linha_estacao
    linha_estacao_data = []

    # Linha 8 (Diamante)
    for ordem, code in enumerate(linhas_dict["L8"], start=1):
        linha_estacao_data.append({
            'id_linha': 8,
            'id_estacao': codigo_to_id[code],
            'ordem': ordem
        })

    # Linha 9 (Esmeralda)
    for ordem, code in enumerate(linhas_dict["L9"], start=1):
        linha_estacao_data.append({
            'id_linha': 9,
            'id_estacao': codigo_to_id[code],
            'ordem': ordem
        })

    op.bulk_insert(linha_estacao_table, linha_estacao_data)


def downgrade() -> None:
    """Downgrade schema."""
    # Deletar na ordem correta (respeitar foreign keys)
    op.execute("DELETE FROM linha_estacao WHERE id_linha IN (8, 9)")
    op.execute("DELETE FROM estacao")
    op.execute("DELETE FROM linha WHERE id IN (8, 9)")
