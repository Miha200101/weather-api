import os
import pandas as pd
import mysql.connector

# Conectare la baza de date
conn = mysql.connector.connect(
    user="root",
    password="Myky2001",
    database="weather_db",
    unix_socket="/var/run/mysqld/mysqld.sock"
)
cursor = conn.cursor()

# Import TG_STAID*.txt
data_folder = "."
files_to_process = [f for f in os.listdir(data_folder) if f.startswith("TG_STAID") and f.endswith(".txt")]
files_to_process.sort()

for filename in files_to_process:
    path = os.path.join(data_folder, filename)
    df = pd.read_csv(path, skiprows=20, sep=",")
    df.columns = [col.strip() for col in df.columns]

    for _, row in df.iterrows():
        staid = int(row["STAID"])
        souid = int(row["SOUID"])
        date = str(row["DATE"])
        # Convert date to YYYY-MM-DD
        date_fmt = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        tg = int(row["TG"]) if row["TG"] != -9999 else None
        q_tg = int(row["Q_TG"]) if "Q_TG" in row and pd.notna(row["Q_TG"]) else None

        cursor.execute("""
            INSERT INTO weather_data (staid, souid, date, tg, q_tg)
            VALUES (%s, %s, %s, %s, %s)
        """, (staid, souid, date_fmt, tg, q_tg))
    print(f"> Imported: {filename}")

# Import stations.txt
stations_path = os.path.join(data_folder, "stations.txt")
if os.path.exists(stations_path):
    with open(stations_path, encoding="utf-8") as f:
        lines = f.readlines()
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("STAID"):
            start_idx = i
            break
    if start_idx is not None:
        df_st = pd.read_csv(stations_path, skiprows=start_idx, sep=",")
        df_st.columns = [col.strip() for col in df_st.columns]
        for _, row in df_st.iterrows():
            staid = int(row["STAID"])
            staname = str(row["STANAME"]).strip()
            cn = str(row["CN"]).strip()
            lat = str(row["LAT"]).strip()
            lon = str(row["LON"]).strip()
            hght = int(row["HGHT"]) if pd.notna(row["HGHT"]) else None

            cursor.execute("""
                INSERT INTO stations (staid, staname, cn, lat, lon, hght)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (staid, staname, cn, lat, lon, hght))
        print("> Imported: stations.txt")
    else:
        print("Header STAID not found in stations.txt")
else:
    print("stations.txt not found!")

conn.commit()
cursor.close()
conn.close()
print("Import complet TG_STAID*.txt + stations.txt")

