import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp=Blueprint('log',__name__,url_prefix='/log')

@bp.route('/logList')
def logList():
    db=get_db()
    if request.method=="GET":
        try:
            logs=db.execute(
                "SELECT * FROM habit_logs"
            ).fetchall()
            return render_template(
                "log/logList.html",
                logs=logs
            )
        except Exception as e:
            return str(e)
    # return render_template("log/logList.html")