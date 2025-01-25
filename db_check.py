import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("stock_data.db")
cursor = conn.cursor()

# Execute SQL commands
cursor.execute("PRAGMA table_info(stock_data);")
print("Table structure:", cursor.fetchall())

cursor.execute("SELECT * FROM stock_data LIMIT 10;")
print("First 10 rows of data:", cursor.fetchall())

# Close the connection
conn.close()
