from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("message_viewer.html")

def get_db():
    con = sqlite3.connect('..\consumer\messaging-database')
    con.row_factory = sqlite3.Row
    return con

@app.route("/messages", methods=["GET"])
def get_messages():
    con = get_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
    rows = cursor.fetchall()
    con.close()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    app.run(debug=True, port=5001)