import mysql.connector
import pandas as pd
import numpy as np
import sqlalchemy

conn = mysql.connector.connect(
    user = 'root',
    password = 'root',
    host = 'localhost',
    database = 'f1'
)

cur = conn.cursor()

cur.execute("SHOW TABLES;")
tables = cur.fetchall()
count = 0
for table in tables:
    count_len = f"SELECT COUNT(*) FROM {table[0]};"
    cur.execute(count_len)
    count += cur.fetchone()[0]
    
print(count)