from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import Session

class DBConn:
    def __init__(self):
        metadata_obj = MetaData()

        Table(
            'users_entity', 
            metadata_obj, 
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('name', String(30), nullable=False),
            Column('last_name', String(50), nullable=False),
        )
        
        Table(
            'address_entity',
            metadata_obj,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('user_id', ForeignKey('users_entity.id'), nullable=False),
            Column('email_address', String, nullable=False),
        )    
        
        self.engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

        metadata_obj.create_all(self.engine)
        
        with Session(self.engine) as session:
            result = session.execute(text('select name from sqlite_master where type="table" order by name'))
            items = result.all()
            ic(items)
