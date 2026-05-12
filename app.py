from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# データベースに接続
# def get_db_connection():
#     conn=sqlite3.connect('/database/Diary.db')
#     conn.row_factory=sqlite3.Row
#     return conn

# データの追加
# @app.route("/",methods=["POST","GET"])
# def index():
#     getup={
#         'year':2026,
#         'month':5,
#         'day':2,
#         'completed':False
#     }
#     # return "POST Method"
#     return render_template(
#         "home_page.html",
#         data=getup
#         )

# @app.route("/send", methods=["POST"])
# def receive():
#     task = request.form["task"]
#     print(task)
#     return "OK"

# @app.route("/api/hoge")
# def api_data():
#     return jsonify({"message":"ok"})

# @app.route("/api/DB",methods=["POST"])
# def db_input():
#     data=request.get_data()
#     print(data)
#     return "",204

# @app.route("/api/DB",methods=['GET'])
# def getDB():
#     # データベースから必要な情報を取る処理を書く
#     pass

# @app.route('/<username>')
# def profile(username):
#     return f'{username}\'s profile'

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('home_page.html',name=name)
    
if __name__ == "__main__":
    app.run()