import pyodbc

class Database:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None

    def connect_database(self):
        cnx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server 
            + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        if self.connection is not None:
            self.connection.close()
        self.connection = cnx
        self.cursor = cnx.cursor()
        return

    def close_database(self):
        if self.connection is not None and self.cursor is not None:
            self.cursor.close()
            self.connection.close()
            self.cursor = None
            self.connection = None
    
    def store_entry(self, host_id, session_id, source_site, dest_site, time):
        insert = ("INSERT INTO self.database (host_id, session_id, source_site, dest_site, time) " + 
                  "VALUES (%(host_id)s, %(session_id)s, %(source_site)s, %(dest_site)s, %(time)s)")
        vals = {
            'host_id': host_id,
            'session_id': session_id,
            'source_site': source_site,
            'dest_site': dest_site,
            'time': time
            }
        self.cursor.execute(insert, vals)
        self.connection.commit()

    def read_entry(self, session_id, time):
        query = ("SELECT (host_id, session_id, source_site, dest_site, time) " +
                 "FROM self.database WHERE (session_id = %(session_id)s AND time=%(time)s")
        self.cursor.execute(query, {'session_id': session_id, 'time': time})
        rows = self.cursor.fetchall()
        return rows


