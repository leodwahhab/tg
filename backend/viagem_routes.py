import datetime

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from dependencies import pegar_sessao
from models import ViagemUsuario, Usuario, Estacao, Ocorrencia, TipoOcorrencia
from schemas import ViagemUsuarioSchema, OcorrenciaSchema, OcorrenciaCreateSchema, TipoOcorrenciaSchema, TipoOcorrenciaCreateSchema
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

@viagem.post("/ocorrencia")
def registrar_ocorrencia(
        ocorrencia_create_schema: OcorrenciaCreateSchema,
        session: Session = Depends(pegar_sessao),
        usuario_autenticado: Usuario = Depends(verificar_token)
):
    """
    Registrar uma ocorrência relacionada a uma viagem.
    O ID do usuário é obtido automaticamente do token JWT.
    """
    try:

        viagem_recente = (session.query(ViagemUsuario).filter(ViagemUsuario.id_usuario == usuario_autenticado.id)
                          .order_by(ViagemUsuario.horario_embarque.desc()).first())

        if not viagem_recente:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma viagem encontrada nas últimas 2 horas"
            )

        duas_horas_atras = datetime.datetime.now() - datetime.timedelta(hours=2)
        if viagem_recente.horario_embarque < duas_horas_atras:
            raise HTTPException(
                status_code=400,
                detail="Embarque em um trem para registrar ocorrência"
            )

        # Verificar se o tipo de ocorrência existe
        tipo_ocorrencia = session.query(TipoOcorrencia).filter(
            TipoOcorrencia.id == ocorrencia_create_schema.id_tipo
        ).first()

        if not tipo_ocorrencia:
            raise HTTPException(
                status_code=400,
                detail="Tipo de ocorrência inválido"
            )

        # Criar nova ocorrência
        nova_ocorrencia = Ocorrencia(
            num_vagao=ocorrencia_create_schema.num_vagao,
            id_tipo=ocorrencia_create_schema.id_tipo,
            data_hora=datetime.datetime.now(),
            valido=True,
            id_viagem=viagem_recente.id_viagem,
            id_usuario_viagem=usuario_autenticado.id
        )
        session.add(nova_ocorrencia)
        session.commit()
        session.refresh(nova_ocorrencia)

        return {
            "status": "Ocorrência registrada com sucesso",
            "id_ocorrencia": nova_ocorrencia.id,
            "tipo": {
                "id": tipo_ocorrencia.id,
                "nome": tipo_ocorrencia.nome
            },
            "num_vagao": nova_ocorrencia.num_vagao,
            "data_hora": nova_ocorrencia.data_hora.isoformat(),
            "id_viagem": viagem_recente.id_viagem,
            "id_usuario": usuario_autenticado.id
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar ocorrência: {str(e)}"
        )

@viagem.get("/tipo-ocorrencia")
def listar_tipos_ocorrencia(
    session: Session = Depends(pegar_sessao),
    usuario_autenticado: Usuario = Depends(verificar_token)
):
    """
    Listar todos os tipos de ocorrência disponíveis.
    """
    tipos = session.query(TipoOcorrencia).order_by(TipoOcorrencia.nome).all()

    return {
        "total": len(tipos),
        "tipos": [
            {
                "id": tipo.id,
                "nome": tipo.nome,
                "descricao": tipo.descricao
            }
            for tipo in tipos
        ]
    }


@viagem.post("/tipo-ocorrencia")
def criar_tipo_ocorrencia(
        tipo_ocorrencia_schema: TipoOcorrenciaCreateSchema,
        session: Session = Depends(pegar_sessao),
        usuario_autenticado: Usuario = Depends(verificar_token)
):
    """
    Criar um novo tipo de ocorrência.
    """
    try:
        novo_tipo = TipoOcorrencia(
            nome=tipo_ocorrencia_schema.nome,
            descricao=tipo_ocorrencia_schema.descricao
        )
        session.add(novo_tipo)
        session.commit()
        session.refresh(novo_tipo)

        return {
            "status": "Tipo de ocorrência criado com sucesso",
            "id_tipo_ocorrencia": novo_tipo.id,
            "nome": novo_tipo.nome,
            "descricao": novo_tipo.descricao
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar tipo de ocorrência: {str(e)}"
        )