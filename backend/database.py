import sqlite3
import os
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            os.path.join(current_app.instance_path, 'app.db')
        )
        g.db.row_factory = sqlite3.Row  # 結果を辞書のように扱えるようにする
        g.db.execute('PRAGMA foreign_keys = ON')  # 外部キー制約を有効にする
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)  # リクエスト終了時に自動でDBを閉じる