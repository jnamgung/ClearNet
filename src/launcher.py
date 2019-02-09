from http import server
from database import Database
import host
import link
from flask import Flask, render_template, request

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

@app.route('/redirect/<host>/<source_platform>/<dest_platform>')
def reroute(host, source_platform, dest_platform):
    return link.reroute(db, host, source_platform, dest_platform)


@app.route('/verify', methods = ['POST', 'GET'])
def verify():
    if request.method == 'POST':
        HID = request.form['username']
        HPW_s = request.form['password']
        if db.host_exists(HID):
            HPW_r = db.get_password(HID)
            if HPW_r is HPW_s:
                return render_template('dashboard.html', value=HID)
        else:
            db.add_host(HID, HPW_s)
            return render_template('dashboard.html', value=HID)
    return

if __name__ == '__main__':
    app.run(debug=True)
