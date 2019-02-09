import pyodbc

class Database:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None
        return

    def connect_database(self):
        cnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=' 
            + self.server + ';Database=' + self.database + ';Uid=' 
            + self.username + ';Pwd=' + self.password
            + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
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
        return
    
    def host_exists(self, host_id):
        return self.cursor.tables(table=host_id, tableType='TABLE').fetchone()

    def add_host(self, host_id):
        if not self.host_exists(host_id):
            self.cursor.execute("CREATE TABLE " + host_id + " (SID INTEGER, "
                + "SSITE VARCHAR(256), DSITE VARCHAR(256), T DATETIME)")
        self.connection.commit()
        return

    def del_host(self, host_id):
        self.cursor.execute("DROP TABLE " + host_id)
        self.connection.commit()
        return
    
    def store_entry(self, host_id, session_id, source_site, dest_site, time):
        query = ("INSERT INTO " + host_id + "(SID, SSITE, DSITE, T) "
            + "VALUES(?, ?, ?, ?)")
        vals = [session_id, source_site, dest_site, time]
        self.cursor.execute(query, *vals)
        self.connection.commit()
        return

    def read_entry(self, host_id, session_id, time):
        query = ("SELECT SID, SSITE, DSITE, T FROM " + host_id + " WHERE "
            + "SID=? AND T=?")
        self.cursor.execute(query, [session_id, time])
        rows = self.cursor.fetchall()
        return rows


