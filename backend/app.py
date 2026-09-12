from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import database
import actions
import diaries
import click
import os

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

database.init_app(app)

@app.cli.command('init-db')
def init_db_command():
    database.init_db()
    click.echo('データベースを初期化しました。')

app.register_blueprint(actions.bp)
app.register_blueprint(diaries.bp)

@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(app.static_folder +'/'+path):
        return send_from_directory(app.static_folder,path)
    return send_from_directory(app.static_folder,'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)