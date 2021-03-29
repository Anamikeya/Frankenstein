import sqlite3 as sql

_db_file='database.db'


class db(object):
    """
    Contextmanager for handling connection to database on disk


    """
    def __init__(self, file=_db_file, *args,**kwargs):
        try:
            print("Connecting db")
            self.db = sql.connect(file)
            print("Connected db")
        except:
            print("Couldnt connect to db")
    def __enter__(self, *args,**kwargs):
        print("Creating instance of db")
        return self.db
    def __exit__(self, type, value, traceback, *args,**kwargs):
        print('Closing db')
        self.db.close()
        print('Closed db')

with db():
    print("innan")
    print(db())
    print("efter")
