import happybase as hb

conn = hb.Connection()

table = conn.table("powers")

columns = (b'personal:hero', b'personal:power', 
           b'professional:name', b'professional:xp',
           b'custom:color')
for key, data in table.scan(columns = columns, include_timestamp=True):
    print('Found: {}, {}'.format(key, data))

conn.close()
