from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# DB接続
def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

# 初期化（テーブル作成）
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

# 取得
@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()
    rows = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# 追加
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    text = data.get("text")

    conn = get_db()
    conn.execute("INSERT INTO todos (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)