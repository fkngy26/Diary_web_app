import psycopg2
import psycopg2.extras
import os
from flask import g, current_app
from dotenv import load_dotenv

load_dotenv()  # .envファイルの内容を読み込む


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            os.environ['DATABASE_URL'],
            cursor_factory=psycopg2.extras.RealDictCursor
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        with db.cursor() as cur:
            cur.execute(f.read().decode('utf8'))
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)