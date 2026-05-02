from flask import Flask, render_template, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

# データベースに接続
# def get_db_connection():
#     conn=sqlite3.connect('/database/Diary.db')
#     conn.row_factory=sqlite3.Row
#     return conn

# データの追加
@app.route("/",methods=["POST","GET"])
def index():
    # return "POST Method"
    return render_template("/home_page.html")

@app.route("/send", methods=["POST"])
def receive():
    task = request.form["task"]
    print(task)
    return "OK"

if __name__ == "__main__":
    app.run()