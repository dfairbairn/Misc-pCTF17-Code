"""

"""

#import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('wigle.sqlite')
cur = conn.cursor()

# Get table entries
cur.execute('''
SELECT * FROM location''')
_ids, bssids, levels, lats, lons, alts, accs, times = [ list() for i in range(8)]
for row in cur.fetchall():
    print(row)
    _id, bssid, level, lat, lon, alt, acc, time = row
    _ids.append(_id); bssids.append(bssid); levels.append(level); lats.append(lat)
    lons.append(lon); alts.append(alt); accs.append(acc); times.append(time)

