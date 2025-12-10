import os
from datetime import timedelta, datetime, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from dependencies import pegar_sessao
from models import Usuario


# carregar envs
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# definir contexto de criptografia e esquema OAuth2
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")


# metodos de autenticação e autorização
def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado")
    usuario_opt = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario_opt:
        raise HTTPException(status_code=401, detail="Usuario invalido")
    return usuario_opt

def autenticar_usuario(session, username, password):
    usuario_opt = session.query(Usuario).filter(Usuario.email == username).first()
    if not usuario_opt:
        raise HTTPException(status_code=400, detail="Email não registrado.")
    if not bcrypt_context.verify(password, usuario_opt.senha):
        raise HTTPException(status_code=400, detail="Email e/ou Senha incorretos(a).")
    return usuario_opt
