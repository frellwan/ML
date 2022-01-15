import happybase as hb
import csv

conn = hb.Connection()

powers = conn.table("powers")
with open("input.csv") as file:
    for row in csv.reader(file):
        data = {
            "personal:hero"     : row[1], "personal:power"  : row[2],
            "professional:name" : row[3], "professional:xp" : row[4],
            "custom:color"      : row[5]
        }
        powers.put(row[0], data)
        
conn.close()
