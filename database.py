import dbm

db = dbm.open('local_links', 'r')

for key in db:
    print(int(key), db[key])


db.close()