from http import server
from database import Database
import host
import link
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

server_url = "clearnet.database.windows.net"
db_string = "ClearNet"
db_username = "server@clearnet"
db_password = "TThacksCN1"

app = Flask(__name__)
db = Database(server_url, db_string, db_username, db_password)
db.connect_database()


@app.route('/')
def login_page():
    return render_template('index.html')


@app.route('/dashboard/<hid>')
def dashboard_page(hid):
    data = db.get_platforms(hid)
    platform_list = []
    for row in data:
        platform_list.append(list(row))
    print(platform_list)
    return render_template('dashboard.html', value=hid, platform_list=platform_list)

@app.route('/dashboard/<hid>/add-platform', methods = ['POST'])
def add_platform(hid):
    pid = request.form['new_plat']
    purl = request.form['new_plat_url']
    db.set_platform(hid, pid, purl)
    return redirect(url_for('.dashboard_page', hid=hid))


@app.route('/redirect/<host>/<source_platform>/<dest_platform>')
def reroute(host, source_platform, dest_platform):
    return link.reroute(db, host, source_platform, dest_platform)


@app.route('/verify', methods=['POST'])
def verify():
    HID = request.form['username']
    HPW_s = request.form['password']
    if db.host_exists(HID):
        HPW_r = db.get_password(HID)
        if HPW_r == HPW_s:
            return redirect(url_for('.dashboard_page', hid=HID))
        else:
            return redirect(url_for('.login_page'))
    else:
        db.add_host(HID, HPW_s)
        return redirect(url_for('.dashboard_page', hid=HID))
    return

@app.route('/delete/<hid>')
def delete_host(hid):
    db.del_host(hid)
    return redirect(url_for('.login_page'))

if __name__ == '__main__':
    app.run(debug=True)
