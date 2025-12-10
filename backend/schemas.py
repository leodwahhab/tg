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


class ViagemUsuarioSchema(BaseModel):
    id_viagem: int
    cod_estacao: str
    horario_embarque: datetime

    class Config:
        from_attributes = True


class TipoOcorrenciaSchema(BaseModel):
    id: int
    nome: str
    descricao: str

    class Config:
        from_attributes = True


class TipoOcorrenciaCreateSchema(BaseModel):
    nome: str
    descricao: str

    class Config:
        from_attributes = True


class OcorrenciaCreateSchema(BaseModel):
    num_vagao: int
    id_tipo: int  # ID do tipo de ocorrência (1-20)

    class Config:
        from_attributes = True


class OcorrenciaSchema(BaseModel):
    id: int
    num_vagao: int
    id_tipo: int
    data_hora: datetime
    valido: bool
    id_viagem: int
    id_usuario_viagem: int

    class Config:
        from_attributes = True