from flask import Flask
from database import Database
from datetime import date
from http import server
from collections import defaultdict

def login (db, username, password):
    return db.get_password(username) is password

def count_relation(db, host, network1, network2, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, '%', network1, network2, startTime, endTime)
    return len(rows)

def count_src(db, host, src, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, '%', src, '%', startTime, endTime)
    return len(rows)

def count_tgt(db, host, tgt, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, '%', '%', tgt, startTime, endTime)
    return len(rows)

def count_usr(db, host, usr, startTime=date.min, endTime=date.max):
    rows = db.read_mult(host, usr, '%', '%', startTime, endTime)
    return len(rows)

def count_unique_accesses(db, session_id, startTime=date.min, endTime=date.max):
    all_networks = defaultdict(int)
    all_accesses = db.read_mult(host, session_id, '%', '%', startTime, endTime)
    for row in range (0, len(all_accesses)-1):
        if (row == 0) or (all_accesses[row][1] != all_accesses[row-1][2]):
                all_networks[all_accesses[row][1]] += 1

    return all_networks 
