from database import Database
from datetime import datetime
from datetime import timedelta

server_url = "clearnet.database.windows.net"
db_string = "ClearNet"
username = "server@clearnet"
password = "TThacksCN1"

azdb = Database(server_url, db_string, username, password)
azdb.connect_database()
azdb.add_host("test_host")

time1 = datetime.now().replace(microsecond=0)
time2 = time1 + timedelta(seconds=2)
time3 = time2 + timedelta(seconds=2)
time4 = time3 + timedelta(minutes=1)

timeInt1 = time1 + timedelta(seconds=8)
timeInt2 = time1 + timedelta(days=1)
azdb.store_entry("test_host", 1, "youtube.com", "google.com", time1)
azdb.store_entry("test_host", 1, "facebook.com", "google.com", time2)
azdb.store_entry("test_host", 2, "youtube.com", "google.com", time1)
azdb.store_entry("test_host", 2, "youtube.com", "stackoverflow.com", time2)
azdb.store_entry("test_host", 3, "facebook.com", "google.com", time3)
azdb.store_entry("test_host", 1, "youtube.com", "stackoverflow.com", time4)
#print(azdb.read_entry("test_host", 1, time1))
print(azdb.read_mult("test_host", '%', "youtube.com", '%', time1, timeInt1))
print(azdb.read_mult('test_host', '%', '%', '%'))

azdb.del_host("test_host")
azdb.close_database()