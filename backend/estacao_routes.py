from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from consulta_estacao import LINHAS, ESTACOES, get_next_train
from dependencies import pegar_sessao
from security import verificar_token
from viagem_service import sincronizar_dados_viagem, get_ocorrencias_viagem

estacao_router = APIRouter(prefix="/estacao", tags=["estacao"], dependencies=[Depends(verificar_token)])

@estacao_router.get("/proximo-trem")
async def proximo_trem(linha: str, estacao: str, session: Session = Depends(pegar_sessao)):
    """
    Exemplo:
    /proximo-trem?linha=L9&estacao=PIN
    """

    if linha not in LINHAS:
        raise HTTPException(
            400,
            detail=f"Linha inválida. Use: {list(LINHAS.keys())}"
        )

    if estacao not in LINHAS[linha]:
        raise HTTPException(
            400,
            detail=f"Estação inválida para linha {linha}. Use: {LINHAS[linha]}"
        )

    if estacao not in ESTACOES:
        raise HTTPException(400, detail="Código de estação desconhecido.")

    # Chamada para a API
    next_train = get_next_train(linha, estacao)

    if not next_train:
        raise HTTPException(404, detail="Nenhum trem encontrado para esta estação no momento.")

    viagem_ids = sincronizar_dados_viagem(session, linha, next_train)
    next_train[0]["viagem_id"] = viagem_ids[0]
    next_train[0]["ocorrencias"] = get_ocorrencias_viagem(session, viagem_ids[0])

    if len(next_train) > 1:
        next_train[1]["viagem_id"] = viagem_ids[1]
        next_train[1]["ocorrencias"] = get_ocorrencias_viagem(session, viagem_ids[1])

    return {
        "linha": linha,
        "estacao_codigo": estacao,
        "estacao_nome": ESTACOES[estacao],
        "proximo_trem": next_train
    }