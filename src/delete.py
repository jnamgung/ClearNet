import pyodbc

server_url = "clearnet.database.windows.net"
db_string = "ClearNet"
username = "server@clearnet"
password = "TThacksCN1"

table_name = '_hosts'

tempcnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server='
                             + server_url + ';Database=' + db_string
                             + ';Uid=' + username + ';Pwd=' + password
                             + ';Encrypt=yes;TrustServerCertificate=no;'
                             + 'Connection Timeout=30')
tempcnx.cursor().execute("DROP TABLE " + table_name)
tempcnx.commit()
tempcnx.close()

table_name = '_p_fuckthis'

tempcnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server='
                             + server_url + ';Database=' + db_string
                             + ';Uid=' + username + ';Pwd=' + password
                             + ';Encrypt=yes;TrustServerCertificate=no;'
                             + 'Connection Timeout=30')
tempcnx.cursor().execute("DROP TABLE " + table_name)
tempcnx.commit()
tempcnx.close()

table_name = 'fuckthis'

tempcnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server='
                             + server_url + ';Database=' + db_string
                             + ';Uid=' + username + ';Pwd=' + password
                             + ';Encrypt=yes;TrustServerCertificate=no;'
                             + 'Connection Timeout=30')
tempcnx.cursor().execute("DROP TABLE " + table_name)
tempcnx.commit()
tempcnx.close()
