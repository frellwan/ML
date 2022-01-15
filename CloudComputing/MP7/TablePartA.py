import happybase as hb

conn = hb.Connection()

powerCols = {"personal" : dict(), 
             "professional": dict(), 
             "custom": dict()}
conn.create_table("powers", powerCols)

foodCols = {"nutrition": dict(), 
            "taste": dict()}
conn.create_table("food", foodCols)

conn.close()
