from flask import Flask
from database import Database
from datetime import date

server = "clearnet.database.windows.net"
database = "ClearNet"
username
password

db = Database(server, database, username, password)
db.connect_database()

def login ():
    pass

def count_relation(db, network1, network2, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, '%', network1, network2, startTime, endTime)
    return length(rows)

def count_src(db, src, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, '%', src, '%', startTime, endTime)
    return length(rows)

def count_tgt(db, tgt, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, '%', '%', tgt, startTime, endTime)
    return length(rows)

def count_usr(db, usr, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, usr, '%', '%', startTime, endTime)
    return length(rows)

#def count_unique_accesses(db, session_id, startTime=date.min, endTime=date.max):
#    all_accesses = db.read_mult(host, session_id, '%', '%')
#    pass
