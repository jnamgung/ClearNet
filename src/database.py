import pyodbc
from datetime import date

hosts_database = '_hosts'


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
                             + self.server + ';Database=' + self.database
                             + ';Uid=' + self.username + ';Pwd=' + self.password
                             + ';Encrypt=yes;TrustServerCertificate=no;'
                             + 'Connection Timeout=30')
        if self.connection is not None:
            self.connection.close()
        self.connection = cnx
        self.cursor = cnx.cursor()

        if not self.cursor.tables(table=hosts_database,
                                  tableType='TABLE').fetchone():
            self.cursor.execute('CREATE TABLE [' + hosts_database
                                + '] (HID VARCHAR(32) PRIMARY KEY, '
                                + 'HPW VARCHAR(32))')
            self.connection.commit()
        return

    def close_database(self):
        if self.connection is not None and self.cursor is not None:
            self.cursor.close()
            self.connection.close()
            self.cursor = None
            self.connection = None
        return

    def host_exists(self, host_id):
        return (self.cursor.tables(table=host_id, tableType='TABLE').fetchone()
                and self.cursor.execute('SELECT EXISTS(SELECT 1 FROM ['
                                        + hosts_database + '] WHERE HID=['
                                        + host_id + '] LIMIT 1)'))

    def add_host(self, host_id, host_pw):
        if not self.host_exists(host_id):
            self.cursor.execute('CREATE TABLE [' + host_id + '] (SID INTEGER, '
                                + 'SSITE VARCHAR(256), DSITE VARCHAR(256), T DATETIME)')
            self.cursor.execute('INSERT INTO [' + hosts_database
                                + '] (HID, HPW) VALUES (?, ?)', [host_id, host_pw])
            self.connection.commit()
        return

    def del_host(self, host_id):
        self.cursor.execute('DELETE FROM [' + hosts_database +
                            '] WHERE HID=\'' + host_id + '\'')
        self.cursor.execute('DROP TABLE [' + host_id + ']')
        self.connection.commit()
        return

    def get_password(self, host_id):
        self.cursor.execute('SELECT HPW FROM [' + hosts_database
                                   + '] WHERE HID=\'' + host_id + '\'')
        return self.cursor.fetchone()[0]

    def set_password(self, host_id, password):
        self.cursor.execute('UPDATE [' + hosts_database + '] SET HPW=? '
                            + 'WHERE HID=?', [password, host_id])
        self.connection.commit()

    def store_entry(self, host_id, session_id, source_site, dest_site, time):
        query = ('INSERT INTO [' + host_id + '] (SID, SSITE, DSITE, T) '
                 + 'VALUES(?, ?, ?, ?)')
        vals = [session_id, source_site, dest_site, time]
        self.cursor.execute(query, *vals)
        self.connection.commit()
        return

    def read_entry(self, host_id, session_id, time):
        query = ('SELECT SID, SSITE, DSITE, T FROM [' + host_id + '] WHERE '
                 + 'SID=? AND T=?')
        self.cursor.execute(query, [session_id, time])
        rows = self.cursor.fetchone()
        return rows

    def read_mult(self, host_id, session_id, source_site, dest_site,
                  start_time=date.min, end_time=date.max):
        query = ('SELECT SID, SSITE, DSITE, T FROM [' + host_id + '] WHERE '
                 + '(SID LIKE ?) AND (SSITE LIKE ?) AND (DSITE LIKE ?) AND '
                 + '(T BETWEEN ? AND ?)')
        self.cursor.execute(query, [session_id, source_site, dest_site,
                                    start_time, end_time])
        rows = self.cursor.fetchall()
        return rows
