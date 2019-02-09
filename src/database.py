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
        cursor = cnx.cursor();
        insert = ("INSERT INTO self.database (host_id, session_id, source_site, dest_site, time)"
                  "VALUES (%(host_id)s, %(session_id)s, %(source_site)s, %(dest_site)s, %(time)s)")
        vals = {
            'host_id': host_id,
            'session_id': session_id,
            'source_site': source_site,
            'dest_site': dest_site,
            'time': time
            }
        cursor.execute(insert, vals)
        cnx.commit()

    def read_entry(self, session_id, requested_time):
        cursor = cnx.cursor();
        query = ("SELECT (host_id, session_id, source_site, dest_site, time)"
                 "FROM self.database WHERE (session_id = %(session_id)s AND time=%(time)s")
        cursor.execute(query, {'session_id': requested_tid, 'time': requested_time})
        rows=cursor.fetchall();
        return rows


