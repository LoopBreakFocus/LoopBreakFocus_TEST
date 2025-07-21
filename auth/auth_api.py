from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib

app = Flask(__name__)
CORS(app)

DB = "users.db"

def create_user_table():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

create_user_table()

def hash_pwd(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (data["name"], data["email"], hash_pwd(data["password"])))
        conn.commit()
        return jsonify({"status": "success", "message": "User created!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Email already exists."}), 409
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
              (data["email"], hash_pwd(data["password"])))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"status": "success", "message": "Login successful", "user_id": user[0]})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)