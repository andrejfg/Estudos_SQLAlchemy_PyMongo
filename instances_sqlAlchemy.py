from sqlalchemy import inspect, create_engine, Column, Integer, String, ForeignKey, select, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
engine = create_engine("sqlite://")


class Cliente(Base):
    # Nome da Tabela - Obrigatório
    __tablename__ = "cliente"

    # Atributos (Colunas) da Tabela - Obrigatório
    # Chave Primária
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(9), unique=True)
    endereco = Column(String(40))

    # Referência de relacionamento e regra de exclusão
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente (id={self.id}, name={self.name}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    # Nome da Tabela
    __tablename__ = "conta_cliente"

    # Atributos (Colunas) da Tabela - Obrigatório
    # Chave Primária
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer, unique=True)
    saldo = Column(Float)
    # Chave Estrangeira
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    # Referência de relacionamento e sem regra de exclusão
    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta (id={self.id}, tipo={self.tipo} ,agencia={self.agencia}, num={self.num}, id_cliente={self.id_cliente}, saldo={self.saldo})"

