from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

class DBConn:
    def __init__(self):
        self.engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
        with Session(self.engine) as session:
            session.execute(text('create table my_table (x int, y int)'))
            session.commit()
            
            session.execute(
                text('insert into my_table (x, y) values (:x, :y)'),
                [{ 'x': 1, 'y': 1 }, { 'x': 2, 'y': 4 }],
            )
            session.commit()
            
            result = session.execute(text('select * from my_table'))
            ic(result.all())
            
            # pass
            # result = session.
