import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute("""
CREATE TABLE test(
id INTEGER PRIMARY KEY,
value INTEGER UNSIGNED)
""")

c.execute("""
INSERT INTO test VALUES(0, 14)
""")

c.execute("""
INSERT INTO test VALUES(1, -5)
""")

c.execute("""SELECT * FROM test""")
print(c.fetchall())
