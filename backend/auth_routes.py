from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies import pegar_sessao
from schemas import UsuarioSchema, LoginSchema
from security import bcrypt_context, verificar_token, criar_token, autenticar_usuario

from models import Usuario
from datetime import timedelta

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """
        endpoint de login
    """

    usuario_opt = autenticar_usuario(session, login_schema.email, login_schema.senha)
    access_token = criar_token(usuario_opt.id)
    refresh_token = criar_token(usuario_opt.id, duracao_token=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """
        endpoint de login
    """
    usuario_opt = autenticar_usuario(session, dados_formulario.username, dados_formulario.password)
    access_token = criar_token(usuario_opt.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

@auth_router.post("/register")
async def register(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """
    endpoint de registro
    """
    usuario_opt = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario_opt:
        raise HTTPException(status_code=400, detail="Email já registrado.")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(nome=usuario_schema.nome, email=usuario_schema.email, senha=senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"message": f"User {novo_usuario.nome} registered successfully."}

@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
    """
    endpoint de refresh token
    """
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }