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
                                + 'HPW VARCHAR(32), SIDC INTEGER)')
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
        self.cursor.execute('SELECT HID FROM [' + hosts_database  + '] WHERE HID=?',
                                        host_id)
        t = self.cursor.fetchone()
        s = self.cursor.tables(table=host_id, tableType='TABLE').fetchone()
        u = self.cursor.tables(table='_p_' + host_id, tableType='TABLE').fetchone()
        return (s and t and u)

    def add_host(self, host_id, host_pw):
        if not self.host_exists(host_id):
            self.cursor.execute('CREATE TABLE [' + host_id + '] (SID INTEGER, '
                                + 'SPID VARCHAR(256), DPID VARCHAR(256), T DATETIME)')
            self.cursor.execute('INSERT INTO [' + hosts_database
                                + '] (HID, HPW, SIDC) VALUES (?, ?, 0)', [host_id, host_pw])
            self.cursor.execute('CREATE TABLE [_p_' + host_id + '] (PID VARCHAR(256) PRIMARY KEY,'
                                + ' DSITE VARCHAR(256))')
            self.connection.commit()
        return

    def del_host(self, host_id):
        self.cursor.execute('DELETE FROM [' + hosts_database +
                            '] WHERE HID=?', host_id)
        self.cursor.execute('DROP TABLE [' + host_id + ']')
        self.cursor.execute('DROP TABLE [_p_' + host_id + ']')
        self.connection.commit()
        return

    def get_password(self, host_id):
        self.cursor.execute('SELECT HPW FROM [' + hosts_database
                            + '] WHERE HID=?', host_id)
        return self.cursor.fetchone()[0]

    def set_password(self, host_id, password):
        self.cursor.execute('UPDATE [' + hosts_database + '] SET HPW=? '
                            + 'WHERE HID=?', [password, host_id])
        self.connection.commit()
        return

    def get_sid(self, host_id):
        self.cursor.execute('SELECT SIDC FROM [' + hosts_database
                            + '] WHERE HID=?', host_id)
        return self.cursor.fetchone()[0]
    
    def inc_sid(self, host_id):
        self.cursor.execute('UPDATE [' + hosts_database + '] SET SIDC=? '
                            + 'WHERE HID=?', [self.get_sid(host_id) + 1, host_id])
        self.connection.commit()
        return

    def set_platform(self, host_id, p_id, dest_url):
        self.cursor.execute('MERGE INTO [_p_' + host_id + '] WITH (HOLDLOCK) AS'
                            + ' target USING (SELECT ? AS PID) AS source ON '
                            + '(target.PID = source.PID) WHEN MATCHED THEN '
                            + 'UPDATE SET target.PID = source.PID, TARGET.DSITE '
                            + '= ? WHEN NOT MATCHED THEN INSERT (PID, DSITE) '
                            + 'VALUES (?, ?);', [p_id, dest_url, p_id, dest_url])
        self.connection.commit()
        return

    def get_platforms(self, host_id, p_id='%'):
        self.cursor.execute('SELECT PID, DSITE FROM [_p_' + host_id + '] WHERE '
                                   + 'PID LIKE ?', p_id)
        return self.cursor.fetchall()

    def del_platform(self, host_id, p_id):
        self.cursor.execute(
            'DELETE FROM [_p_' + host_id + '] WHERE PID=?', p_id)
        return

    def store_entry(self, host_id, session_id, source_platform, dest_platform, time):
        query = ('INSERT INTO [' + host_id + '] (SID, SPID, DPID, T) '
                 + 'VALUES(?, ?, ?, ?)')
        vals = [session_id, source_platform, dest_platform, time]
        self.cursor.execute(query, *vals)
        self.connection.commit()
        return

    def read_entry(self, host_id, session_id, time):
        query = ('SELECT SID, SPID, DPID, T FROM [' + host_id + '] WHERE '
                 + 'SID=? AND T=?')
        self.cursor.execute(query, [session_id, time])
        rows = self.cursor.fetchone()
        return rows

    def read_mult(self, host_id, session_id='%', source_platform='%', dest_platform='%',
                  start_time=date.min, end_time=date.max):
        query = ('SELECT SID, SPID, DPID, T FROM [' + host_id + '] WHERE '
                 + '(SID LIKE ?) AND (SPID LIKE ?) AND (DPID LIKE ?) AND '
                 + '(T BETWEEN ? AND ?)')
        self.cursor.execute(query, [session_id, source_platform, dest_platform,
                                    start_time, end_time])
        rows = self.cursor.fetchall()
        return rows
