from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# データベースに接続
# def get_db_connection():
#     conn=sqlite3.connect('/database/Diary.db')
#     conn.row_factory=sqlite3.Row
#     return conn

# データの追加
@app.route("/",methods=["POST"])
def index():
    # return "POST Method"
    return render_template("/home_page.html")

if __name__ == "__main__":
    app.run()