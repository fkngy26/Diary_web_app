import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp=Blueprint('habits',__name__,url_prefix='/habits')

@bp.route('/list',methods=['GET','POST'])
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
    # POST
    if request.method=="POST":
      action=request.form["action"]

      # Habit追加のページを渡す
      if action=="add":
        obj=db.execute(
          'SELECT * FROM habit'
        ).fetchall()
        for a in obj:
          print(dict(a))


        # edit.htmlで使用する最低限のデータを渡しておきたい
        default_habit_obj={
          'habit_name':""
        }
        return render_template(
          'habits/edit.html',
          habit_obj=default_habit_obj
        )

      # Habitのリストから戻る
      elif action=="back":
        # db.execute(
        #   'UPDATE habit SET is_active = 0'
        # )
        # check_list=request.form.getlist('habit_ids')
        # if check_list:
        #   db.execute(
        #     # WHERE id IN (?, ?, ?)を作っている
        #     f'UPDATE habit SET is_active =1 WHERE id IN ({",".join("?"*len(check_list))})',
        #     check_list
        #   )
        # db.commit()
        return redirect(url_for('today.writeTodayDiary'))
      
      elif action=="save":
        print("save")
    
    # GET
    db_habits=db.execute(
      'SELECT * FROM habit'
    ).fetchall()
    if db_habits:
    # habits=[row[1] for row in db_tasks]
      return render_template(
        'habits/list.html',
        habits=db_habits
      )
    else:
      return "タスクが存在しません"
  
  except Exception as e:
    return str(e)
  
@bp.route('/<int:habit_id>',methods=["GET","POST"])
def habit_id(habit_id):
  db=get_db()

  try:
    # POST
    if request.method=="POST":
      pass
    
    # GET
    habit_obj=db.execute(
      'SELECT * FROM habit WHERE id=(?)',(habit_id,)
    ).fetchone()
    return render_template(
      'habits/edit.html',
      habit_obj=habit_obj
    )
  
  except Exception as e:
    return str(e)