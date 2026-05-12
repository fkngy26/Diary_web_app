import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('today', __name__, url_prefix='/today')

@bp.route('/writeTodayDiary',methods=['GET','POST'])
def writeTodayDiary():
  db=get_db()
  if request.method=='POST':
    task=request.form.getlist('habit_ids')
    error=None

    try:
      # 
      placeholder=",".join("?"*len(task))
      activeTasks=db.execute(
        f"SELECT * FROM habit WHERE id IN ({placeholder})",
        task
      ).fetchall()
      for a in activeTasks:
        print(a["habit_name"])
      # print([a[0] for a in activeTasks])
    except Exception as e:
      print(str(e))

    # if not task:
    #   error='task is required'
    
    # if error is None:
    #   try:
    #     # SQL文を挿入している
    #     db.execute(
    #       "INSERT INTO task (task) VALUE (?,?)",
    #       (task)
    #     )
    #     db.commit()
    #   except Exception as e:
    #     error='unexcepted error'
    #   else:
    #     return redirect(url_for("diary_list/list.html"))
    
    # flash(error)

  try:
    db_tasks=db.execute(
      'SELECT * FROM habit WHERE is_active = 1'
    ).fetchall()
    return render_template(
      'today/writeTodayDiary.html',
      habits=db_tasks
    )
  except Exception as e:
    return str(e)