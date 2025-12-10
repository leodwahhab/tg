from pydantic import BaseModel
from datetime import datetime

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True


class ViagemSchema(BaseModel):
    id_viagem: int
    id_estacao: int
    horario_embarque: datetime

    class Config:
        from_attributes = True
