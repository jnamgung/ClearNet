# Handle all end user transactions through link
from flask import redirect
from database import Database

def reroute(db, host, source_platform, dest_platform):
    db.store_entry(host, db.get_sid(host), source_platform, dest_platform)
    db.inc_sid(host)
    return redirect(db.get_platforms(host, dest_platform)[0][1])
