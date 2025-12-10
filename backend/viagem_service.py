from datetime import datetime, date
from sqlalchemy.orm import Session


def sincronizar_dados_viagem(db: Session, linha_codigo: str, dados_api: list):
    """
    Sincroniza os dados de viagem da API com o banco de dados local.
    """
    from models import Linha, Viagem

    linha = db.query(Linha).filter(Linha.numero == int(linha_codigo[1])).first()
    if not linha:
        raise ValueError(f"Linha com código {linha_codigo} não encontrada no banco de dados.")

    viagem_ids = []

    for viagem_dados in dados_api:
        viagem = (db.query(Viagem).filter(Viagem.id_linha == linha.id)
                      .filter(Viagem.sentido == viagem_dados.get("estacao_destino"))
                      .filter(Viagem.horario_chegada_api == viagem_dados.get("hora_previsto_chegada"))
                      .filter(Viagem.data_referencia == date.today())
                      .first())

        if not viagem:
            viagem = Viagem(
                id_linha=linha.id,
                sentido=viagem_dados.get("estacao_destino"),
                horario_chegada_api=viagem_dados.get("hora_previsto_chegada"),
                data_referencia=date.today(),
                status=viagem_dados.get("status"),
                updated_at=datetime.now()
            )
            db.add(viagem)
            db.commit()
        else:
            viagem.status = viagem_dados.get("status")
            viagem.updated_at = datetime.now()
            db.commit()
        viagem_ids.append(viagem.id)
        db.refresh(viagem)
    return viagem_ids