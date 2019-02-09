# Handle all end user transactions through link
from flask import redirect, request, make_response
from database import Database
from datetime import datetime

def reroute(db, host, source_platform, dest_platform):
    sid = None
    if not request.cookies.get(host):
        store_sid = make_response('Storing User ID')
        sid = db.get_sid(host)
        db.inc_sid(host)
        store_sid.set_cookie(host, str(sid))
    else:
        sid = request.cookies[host]

    db.store_entry(host, sid, source_platform, dest_platform, datetime.now().replace(microsecond=0))
    end_link = db.get_platforms(host, dest_platform)[0][1]
    if 'http' not in end_link:
        end_link = 'http://' + end_link
    return redirect(end_link)
