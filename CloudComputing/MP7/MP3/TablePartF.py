import happybase as hb

conn = hb.Connection()

# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER

powers = conn.table("powers")

columns = (b'custom:color', b'professional:name', b'personal:power')

for key, data in powers.scan(columns=columns, include_timestamp=True):
    color = data[b"custom:color"][0]
    name = data[b"professional:name"][0]
    power = data[b"personal:power"][0]  
    
    for key1, data1 in powers.scan(columns=columns, include_timestamp=True):
        color1 = data1[b"custom:color"][0]
        name1 = data1[b"professional:name"][0]
        power1 = data1[b"personal:power"][0]
        
        if color == color1:
            if name != name1:
                print('{}, {}, {}, {}, {}'.format(name, power, name1, power1, color))

conn.close()
