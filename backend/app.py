from flask import Flask, jsonify
from flask_cors import CORS
import database
import click
import os
import actions
import diaries

app = Flask(__name__, instance_relative_config=True)
CORS(app)

# instanceフォルダがなければ作成
os.makedirs(app.instance_path, exist_ok=True)

database.init_app(app)
app.register_blueprint(actions.bp)
app.register_blueprint(diaries.bp)

@app.cli.command('init-db')  # コマンドラインから初期化できるようにする
def init_db_command():
    database.init_db()
    click.echo('データベースを初期化しました。')

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)