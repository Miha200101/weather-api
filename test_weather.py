import mysql.connector

def print_table(header, rows):
    print("\t".join(header))
    for row in rows:
        print("\t".join(str(item) for item in row))

conn = mysql.connector.connect(
    user="root",
    password="Myky2001",
    database="weather_db",
    unix_socket="/var/run/mysqld/mysqld.sock"
)
cursor = conn.cursor()

# Pentru weather_data
cursor.execute("SELECT * FROM weather_data LIMIT 5")
header = [i[0] for i in cursor.description]
rows = cursor.fetchall()
print("Tabelul weather_data:")
print_table(header, rows)
print()

# Pentru stations
cursor.execute("SELECT * FROM stations LIMIT 5")
header = [i[0] for i in cursor.description]
rows = cursor.fetchall()
print("Tabelul stations:")
print_table(header, rows)

cursor.close()
conn.close()

