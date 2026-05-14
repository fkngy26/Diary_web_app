import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import datetime

bp = Blueprint('today', __name__, url_prefix='/today')

@bp.route('/writeTodayDiary',methods=['GET','POST'])
def writeTodayDiary():
  db=get_db()
  if request.method=='POST':
    try:
      today=datetime.datetime.today().date()
      task=request.form.getlist('habit_ids')
      if task:
        placeholder=",".join("?"*len(task))
        activeTasks=db.execute(
          f"SELECT * FROM habit WHERE id IN ({placeholder})",
          task
        ).fetchall()

        # task_logはidで管理する。※同じ名前を使用しても問題ないように
        task_objects=[]
        for task in activeTasks:
          task_object=[]
          task_object.append(task['id'])
          task_object.append(today)
          task_objects.append(task_object)
        db.executemany(
          "INSERT INTO habit_logs ( habit_id, date) VALUES (?,?)",
          task_objects
        )
      diary_text=request.form.get('diary')
      print(diary_text)
      if diary_text:
        db.execute(
          "INSERT INTO diary ( date, diary_text) VALUES (?,?)",
          (today,diary_text)
        )
      db.commit()
      diaries=db.execute(
        "SELECT * FROM diary"
      ).fetchall()
      for d in diaries:
        print(d['diary_text'])

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
      habits=db_tasks,
    )
  except Exception as e:
    return str(e)