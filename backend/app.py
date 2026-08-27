from flask import Flask, jsonify
from flask_cors import CORS
import database
import actions
import diaries
import click

app = Flask(__name__)  # instance_relative_config=True や static_folder はそのまま残してOK
CORS(app)

database.init_app(app)

@app.cli.command('init-db')
def init_db_command():
    database.init_db()
    click.echo('データベースを初期化しました。')

app.register_blueprint(actions.bp)
app.register_blueprint(diaries.bp)

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)