from sqlalchemy import text, insert, MetaData, Table
from database import sync_engine, session_factory, Base
from models import metadata_object, workers_table, WorkerOrm




def create_tables():
    sync_engine.echo = False
    metadata_object.drop_all(sync_engine)
    metadata_object.create_all(sync_engine)
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True


'''
def insert_data():
    with sync_engine.connect() as conn:
        # statement = """
        #     INSERT INTO workers (username)
        #     VALUES ('Bober'), ('Volk');
        # """
        # conn.execute(text(statement))

        statement = insert(workers_table).values(
            [
                {'username': 'bobra'},
                {'username': 'voka'},
            ]
        )

        conn.execute(statement)
        conn.commit()
'''

# declarative?
def insert_data():

    with session_factory() as session:
        worker_bobr = WorkerOrm(username='bobr')
        worker_volk = WorkerOrm(username='volk')
        # session.add(worker_bobr)
        # session.add(worker_volk)
        session.add_all([worker_bobr, worker_volk])
        session.commit()
