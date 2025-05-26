from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL connection config
db_config = {
    'host': 'localhost',
    'user': 'root',         # Change as needed
    'password': '1234',     # Change as needed
    'database': 'lab-monitor'
}

@app.route('/')
def dashboard():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Track_ID, Duration FROM PrimaryTable")
    rows = cursor.fetchall()
    conn.close()

    track_count = len(rows)
    tracks = rows

    return render_template('home.html', track_count=track_count, tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)
