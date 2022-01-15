import happybase as hb

conn = hb.Connection()

powers = conn.table("powers")

row1 = powers.row("row1")
row19 = powers.row("row19")

print("hero: {0}, power: {1}, name: {2}, xp: {3}, color: {4}".format(
    row1[b"personal:hero"], row1[b"personal:power"], row1[b"professional:name"],
    row1[b"professional:xp"], row1[b"custom:color"]
))
print("hero: {0}, color: {1}".format(
    row19[b"personal:hero"], row19[b"custom:color"]
))
print("hero: {0}, name: {1}, color: {2}".format(
    row1[b"personal:hero"], row1[b"professional:name"], row1[b"custom:color"]
))

conn.close()
