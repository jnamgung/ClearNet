# Store and retreive information from a MySQL server
import mysql.connector as mysql

def connect_database():
    db = mysql.connector.connect(user="server", database="")

def store_entry(user_id, source_site dest_site):
    pass
