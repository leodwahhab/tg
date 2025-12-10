from fastapi import HTTPException, APIRouter, Depends

from consulta_estacao import LINHAS, ESTACOES, get_next_train
from security import verificar_token

estacao_router = APIRouter(prefix="/estacao", tags=["estacao"], dependencies=[Depends(verificar_token)])

@estacao_router.get("/proximo-trem")
def proximo_trem(linha: str, estacao: str):
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

    return {
        "linha": linha,
        "estacao_codigo": estacao,
        "estacao_nome": ESTACOES[estacao],
        "proximo_trem": next_train
    }