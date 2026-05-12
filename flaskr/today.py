import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('today', __name__, url_prefix='/today')

@bp.route('/writeTodayDiary',methods=['GET','POST'])
def writeTodayDiary():
  if request.method=='POST':
    task=request.form['task']
    diary=request.form['diary']
    db=get_db()
    error=None
    print(task)
    print(diary)
    print("Yes")

    if not task:
      error='task is required'
    
    if error is None:
      try:
        # SQL文を挿入している
        db.execute(
          "INSERT INTO task (task) VALUE (?,?)",
          (task)
        )
        db.commit()
      except Exception as e:
        error='unexcepted error'
      else:
        return redirect(url_for("diary_list/list.html"))
    
    flash(error)

  return render_template('today/writeTodayDiary.html')