import pyodbc

class Database:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect_database(self):
        cnx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server 
            + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        if self.connection is not None:
            self.connection.close()
        self.connection = cnx.cursor()
        return

    def close_database(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
    
    def store_entry(self, host_id, session_id, source_site, dest_site, time):
        self.connection.execute()
        self.connection.commit()

    def read_entry(self, t_id):
        pass
