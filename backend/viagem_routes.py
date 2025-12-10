from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from dependencies import pegar_sessao
from models import ViagemUsuario, Usuario, Estacao
from schemas import ViagemUsuarioSchema
from security import verificar_token

viagem = APIRouter(prefix="/viagem", tags=["viagem"])

@viagem.post("/embarque")
async def registrar_embarque(
    viagem_usuario_schema: ViagemUsuarioSchema,
    session: Session = Depends(pegar_sessao),
    usuario_autenticado: Usuario = Depends(verificar_token)
):
    """
    Registrar o embarque de um usuário em uma viagem.
    O ID do usuário é obtido automaticamente do token JWT.
    """
    try:
        # Verificar se já existe um embarque para esta viagem e usuário
        embarque_existente = session.query(ViagemUsuario).filter(
            ViagemUsuario.id_usuario == usuario_autenticado.id,
            ViagemUsuario.id_viagem == viagem_usuario_schema.id_viagem
        ).first()

        if embarque_existente:
            raise HTTPException(
                status_code=400,
                detail="Usuário já registrado nesta viagem"
            )

        estacao = session.query(Estacao).filter(Estacao.codigo == viagem_usuario_schema.cod_estacao).first()

        # Criar novo embarque usando o ID do usuário autenticado
        novo_embarque = ViagemUsuario(
            id_usuario=usuario_autenticado.id,  # ID obtido do token
            id_viagem=viagem_usuario_schema.id_viagem,
            id_estacao=estacao.id,
            horario_embarque=viagem_usuario_schema.horario_embarque
        )
        session.add(novo_embarque)
        session.commit()
        session.refresh(novo_embarque)

        return {
            "status": "Embarque registrado com sucesso",
            "id_usuario": usuario_autenticado.id,
            "id_viagem": viagem_usuario_schema.id_viagem,
            "id_estacao": estacao.id,
            "horario_embarque": viagem_usuario_schema.horario_embarque
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar embarque: {str(e)}"
        )
