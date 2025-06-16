from flask import Flask, render_template, jsonify
import mysql.connector
import pandas as pd

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Myky2001",
        database="weather_db"
    )

@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT staid, staname FROM stations")
    stations = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(stations)
    return render_template("home.html", data=df[["staid", "staname"]].to_html(index=False))

@app.route("/api/v1/<station>/<date>")
def api(station, date):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tg FROM weather_data
        WHERE staid = %s AND date = %s
    """, (station, date))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row or row["tg"] == -999.9:
        temperature = "LOST"
    else:
        temperature = row["tg"] / 10
    return {"station": station, "date": date, "temperature": temperature}

@app.route("/api/v1/<station>")
def all_data(station):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT date, tg FROM weather_data
        WHERE staid = %s
    """, (station,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    for entry in results:
        if entry["tg"] == -999.9:
            entry["tg"] = "LOST"
        else:
            entry["tg"] = entry["tg"] / 10
    return jsonify(results)

@app.route("/api/v1/yearly/<station>/<year>")
def on_year(station, year):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT date, tg FROM weather_data
        WHERE staid = %s AND date LIKE %s
    """, (station, f"{year}%"))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    for entry in results:
        if entry["tg"] == -999.9:
            entry["tg"] = "LOST"
        else:
            entry["tg"] = entry["tg"] / 10
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

