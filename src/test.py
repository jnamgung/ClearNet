from database import Database
from datetime import datetime
from datetime import timedelta
import host
server_url = "clearnet.database.windows.net"
db_string = "ClearNet"
username = "server@clearnet"
password = "TThacksCN1"

host_id = "fuckthis"

azdb = Database(server_url, db_string, username, password)
azdb.connect_database()
azdb.add_host(host_id, "test_password")

time1 = datetime.now().replace(microsecond=0)
time2 = time1 + timedelta(seconds=2)
time3 = time2 + timedelta(seconds=2)
time4 = time3 + timedelta(minutes=1)

#------------------------------------------------------------------------------
#print(azdb.get_sid(host_id))
#for x in range (0, 5):
#    azdb.inc_sid(host_id)
#    print(azdb.get_sid(host_id))

#azdb.set_platform(host_id, "Instagram", "instagram.com")
#azdb.set_platform(host_id, "Instagram", "instagram.com")
#azdb.set_platform(host_id, "Facebook", "facebook.com")
#azdb.set_platform(host_id, "Twitter", "twitter.com")
#azdb.set_platform(host_id, "Andrew", "andrew.cmu.edu")
#print (azdb.get_platforms(host_id))
#passed------------------------------------------------------------------------

timeInt1 = time1 + timedelta(seconds=8)
timeInt2 = time1 + timedelta(days=1)
azdb.store_entry(host_id, 1, "Youtube", "Google", time1)
azdb.store_entry(host_id, 1, "Facebook", "Google", time2)
azdb.store_entry(host_id, 2, "Youtube", "Google", time1)
azdb.store_entry(host_id, 2, "Youtube", "StackOverflow", time2)
azdb.store_entry(host_id, 1, "Facebook", "Google", time3)
azdb.store_entry(host_id, 1, "Youtube", "StackOverflow", time4)

#------------------------------------------------------------------------------
#print(azdb.read_mult(host_id, '%', "Youtube", '%', time1, timeInt1))
#print(azdb.read_mult(host_id, '%', '%', '%'))
#passed------------------------------------------------------------------------

print(host.count_relation(azdb, host_id, "Youtube", "Google"))
print(host.count_src(azdb, host_id, "Facebook"))
print(host.count_tgt(azdb, host_id, "StackOverflow"))
print(host.count_usr(azdb, host_id, 2));
print(host.count_unique_accesses(azdb, host_id, 1));

print(azdb.get_password(host_id))
azdb.set_password(host_id, 'newpws')
print(azdb.get_password(host_id))

azdb.del_host(host_id)
azdb.close_database()