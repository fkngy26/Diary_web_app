import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp=Blueprint('habits',__name__,url_prefix='/habits')

@bp.route('/edit',methods=['GET','POST'])
def edit():
  db=get_db()
  # db.execute(
  #   'INSERT INTO habit (habit_name,is_active) VALUES(?,?)',
  #   ('getUp',1)
  # )
  # db.commit()

  # 全削除
  # db.execute(
  #   'DELETE FROM habit'
  # )
  # db.commit()

  try:
    if request.method=="POST":
      db.execute(
        'UPDATE habit SET is_active = 0'
      )
      check_list=request.form.getlist('habit_ids')
      if check_list:
        db.execute(
          # WHERE id IN (?, ?, ?)を作っている
          f'UPDATE habit SET is_active =1 WHERE id IN ({",".join("?"*len(check_list))})',
          check_list
        )
      db.commit()
      return redirect(url_for('today.writeTodayDiary'))
  except Exception as e:
    return str(e)

  try:
    db_tasks=db.execute(
      'SELECT * FROM habit'
    ).fetchall()
    # habits=[row[1] for row in db_tasks]
    return render_template(
      'habits/edit.html',
      habits=db_tasks
    )
  except Exception as e:
    return str(e)