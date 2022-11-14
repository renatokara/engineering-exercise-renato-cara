import os
import MySQLdb

class DatabaseSingletonMeta(type):
    """
        Creates the Meta boilerplate for DatabaseSingleton
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseSingleton(metaclass=DatabaseSingletonMeta):
    """
        DatabaseSingleton that create the connection and handles theparameter
        for handling MySql connections
    """
    db = None

    def create(self):

        #TODO for the purpose of this exercise its a good idea to connect every new request
        # but  in a larger project a lib that has connection pools and pool of threads
        # Would be preferable
        mydql_root_password = os.getenv('MYSQL_ROOT_PASSWORD')
        mydql_database = os.getenv('MYSQL_DATABASE')
        mydql_user = os.getenv('MYSQL_USER')
        mydql_port = os.getenv('MYSQL_PORT')
        mydql_host = os.getenv('MYSQL_HOST')
        self.db=MySQLdb.connect(host=mydql_host,user=mydql_user,
                  passwd=mydql_root_password,db=mydql_database,port=int(mydql_port))

        return self.db
       
    def conn(self):
        return self.db

    def cursor(self):
        """
        Returns Cursor object cursors.Cursor
        """
        return self.db.cursor()

    def close(self) -> None :
        self.db.close()

    def rollback(self):
        self.db.rollback()