from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

USERNAME = 'root'
PASSWORD = 'ssafy'
HOST = '127.0.0.1'
PORT = 3306
DBNAME = '007'

DB_URL = 'mysql+pymysql://root:ssafy@localhost:3306/007'

class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    async def connection(self):
        conn = self.engine.connect()
        return conn