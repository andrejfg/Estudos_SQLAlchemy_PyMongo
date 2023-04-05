import pprint

import pymongo as pymongo
from sqlalchemy import inspect, select
from sqlalchemy.orm import Session
import instances_sqlAlchemy


if __name__ == '__main__':
    Base = instances_sqlAlchemy.Base
    engine = instances_sqlAlchemy.engine
    Cliente = instances_sqlAlchemy.Cliente
    Conta = instances_sqlAlchemy.Conta

    Base.metadata.create_all(engine)
    inspector_engine = inspect(engine)
    print(inspector_engine.get_table_names())

    with Session(engine) as session:
        andre = Cliente(
            name='André',
            cpf='153478965',
            endereco='rua 2, casa 33',
            conta=[Conta(tipo='corrente',
                           agencia=1,
                           saldo=1000.0,
                           num=756471)]
        )

        pedro = Cliente(
            name='Pedro',
            cpf='698478965',
            endereco='rua 5, casa 50',
            conta=[Conta(tipo='corrente',
                           agencia=1,
                           saldo=0,
                           num=756741),
                     Conta(tipo='poupanca',
                           saldo=500.0,
                           agencia=1,
                           num=756881)]
        )

        joao = Cliente(
            name='José',
            cpf='153471585',
            endereco='rua 7, casa 1',
        )

        # Enviando para o Banco de dados (persistência de dados)
        session.add_all([andre, pedro, joao])

        session.commit()

    print('estabelecendo uma query para Clientes')
    stmt = select(Cliente)
    print(stmt)
    for cliente in session.scalars(stmt):
        print(cliente)

    print('estabelecendo uma query para Conta')
    stmt = select(Conta)
    print(stmt)
    for conta in session.scalars(stmt):
        print(conta)

    print('estabelecendo uma query para Conta')
    stmt_join = select(Cliente.name,
                       Cliente.cpf,
                       Cliente.endereco,
                       Conta.tipo,
                       Conta.agencia,
                       Conta.num,
                       Conta.saldo).join_from(Cliente, Conta)
    connection = engine.connect()
    results = connection.execute(stmt_join).fetchall()
    mongo_list = list()
    for result in results:
        dado_cliente = list(result)
        mongo_data= {"nome":dado_cliente[0],
                     "cpf":dado_cliente[1],
                     "endereco": dado_cliente[2],
                     "tipo":dado_cliente[3],
                     "agencia":dado_cliente[4],
                     "num": dado_cliente[5],
                     "saldo": dado_cliente[6]
                     }
        mongo_list.append(mongo_data)



    client = pymongo.MongoClient(
        'MongoDB-URI')
    db = client.banco
    clientes_contas = db.clientes_contas
    clientes_contas.insert_many(mongo_list)

    for cliente_conta in clientes_contas.find():
        pprint.pprint(cliente_conta)
