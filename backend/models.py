from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        create_engine, Double)
from sqlalchemy.orm import declarative_base, relationship

db = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    senha = Column(String(255), nullable=False)

    viagens = relationship('ViagemUsuario', back_populates='usuario', cascade='all, delete-orphan')
    localizacoes = relationship('Localizacao', back_populates='usuario', cascade='all, delete-orphan')
    ocorrencias = relationship('Ocorrencia', back_populates='usuario', cascade='all, delete-orphan')


class Linha(Base):
    __tablename__ = 'linha'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(Integer, nullable=False)
    numero = Column(Integer, nullable=False)
    cor_hex = Column(String(6), nullable=False)

    estacoes = relationship('LinhaEstacao', back_populates='linha', cascade='all, delete-orphan')
    viagens = relationship('Viagem', back_populates='linha', cascade='all, delete-orphan')


class Estacao(Base):
    __tablename__ = 'estacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)

    linhas = relationship('LinhaEstacao', back_populates='estacao', cascade='all, delete-orphan')
    embarques = relationship('ViagemUsuario', back_populates='estacao')


class LinhaEstacao(Base):
    __tablename__ = 'linha_estacao'

    id_linha = Column(Integer, ForeignKey('linha.id'), primary_key=True)
    id_estacao = Column(Integer, ForeignKey('estacao.id'), primary_key=True)
    ordem = Column(Integer, nullable=False)

    linha = relationship('Linha', back_populates='estacoes')
    estacao = relationship('Estacao', back_populates='linhas')


class Viagem(Base):
    __tablename__ = 'viagem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_partida_prevista = Column(DateTime, nullable=False)
    sentido = Column(String(50), nullable=False)
    id_linha = Column(Integer, ForeignKey('linha.id'), nullable=False)

    linha = relationship('Linha', back_populates='viagens')
    passageiros = relationship('ViagemUsuario', back_populates='viagem', cascade='all, delete-orphan')


class ViagemUsuario(Base):
    __tablename__ = 'viagem_usuario'

    id_viagem = Column(Integer, ForeignKey('viagem.id'), primary_key=True)
    id_estacao = Column(Integer, ForeignKey('estacao.id'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    horario_embarque = Column(DateTime, nullable=False)

    viagem = relationship('Viagem', back_populates='passageiros')
    estacao = relationship('Estacao', back_populates='embarques')
    usuario = relationship('Usuario', back_populates='viagens')


class Localizacao(Base):
    __tablename__ = 'localizacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    data = Column(DateTime, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    usuario = relationship('Usuario', back_populates='localizacoes')


class Ocorrencia(Base):
    __tablename__ = 'ocorrencia'

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_vagao = Column(Integer, nullable=False)
    tipo = Column(String(50), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    valido = Column(Boolean, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    usuario = relationship('Usuario', back_populates='ocorrencias')
