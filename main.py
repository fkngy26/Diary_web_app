from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# DBファイルのパスを環境変数から取得できるようにする（Renderの永続ディスク用）
# 指定がない場合はカレントディレクトリの todo.db を使用
DB_PATH = os.environ.get("DATABASE_URL", "todo.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL
            )
        """)

# RenderなどのPaaSでは、起動時に明示的に初期化を走らせるのが安全
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()
    rows = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    conn = get_db()
    conn.execute("INSERT INTO todos (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# ローカル実行用。Render上ではGunicornがこの app を直接呼び出すためここは通りません。
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)