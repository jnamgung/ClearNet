# Connection and disconnection
def connect_database():
    pass

def close_database():
    pass


# Interfacing with MySQL data
def store_entry(host_id, session_id, source_site, dest_site, time):
    pass

def read_entry(host_id, session_id, source_site, dest_site, time):
    pass

# Counting data

# Total visits of a site
def count_site_visits(host_id, session_id, counted_site, start_time, end_time):
    pass

#Total inter-site visits by single session
def count_session_visits(host_id, session_id, start_time, end_time):
    pass

#Total link uses
def count_link_visits(host_id, session_id, source_site, dest_site, start_time, end_time):
    pass

# Analysis of data

def most_popular_site(host_id, start_time, end_time):
    pass

def most_popular_path(host_id, start_time, end_time):
    pass

def most_active_time(host_id):
    pass





