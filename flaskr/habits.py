import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import datetime

bp=Blueprint('habits',__name__,url_prefix='/habits')

@bp.route('/add',methods=['GET','POST'])
def add():
  db=get_db()
  if request.method=="POST":
    action=request.form["action"]

    # Habit追加のページを渡す
    if action=="add":
      row_habit_obj={
        'habit_name':request.form.get('habit_name'),
        'repeat_interval':request.form.get('repeat_interval'),
        'is_end':1 if request.form.get('is_end')=="on" else 0,
        'end_date':request.form.get('habitEndDate'),
        'start_date':str(datetime.date.today())
      }
      # Noneを省きたい
      habit_obj={k:v for k,v in row_habit_obj.items() if v != "" and v is not None}
      row_key=habit_obj.keys()
      values=tuple(habit_obj.values())

      placeholders=', '.join(['?']*len(habit_obj))
      columns=', '.join(row_key)
      sql=f'INSERT INTO habit ({columns}) VALUES({placeholders})'
      db.execute(sql,values)
      db.commit()
      return redirect(url_for('habits.list'))
    
    elif action=="cancel":
      return redirect(url_for('habits.list'))
  
  # GET
  add_default_obj={
    'habit_name':'',
    'repeat_interval':1,
    'is_end':0
  }
  return render_template(
    'habits/add.html',
    habit_obj=add_default_obj
  )

@bp.route('/list',methods=['GET','POST'])
def list():
  db=get_db()
  if request.method=="POST":
    action=request.form["action"]
    if action=="back":
      return redirect(url_for('today.writeTodayDiary'))
    if action=="add":
      return redirect(url_for('habits.add'))

  # GET
  db_habits=db.execute(
    'SELECT * FROM habit'
  ).fetchall()
  for i in db_habits:
    print(dict(i))
  return render_template(
    'habits/list.html',
    habits=db_habits
  )
  
@bp.route('/<int:habit_id>',methods=["GET","POST"])
def edit(habit_id):
  db=get_db()
  try:
    # POST
    if request.method=="POST":
      action=request.form["action"]

      if action=="cancel":
        return redirect(url_for('habits.list'))
      
      elif action=="save":
        row_habit_obj={
          'habit_name':request.form.get('habit_name'),
          'repeat_interval':request.form.get('repeat_interval'),
          'is_end':1 if request.form.get('is_end')=="on" else 0,
          'end_date':request.form.get('habitEndDate')
        }
        print(dict(row_habit_obj))
        habit_columns=[f"{k}=?" for k in row_habit_obj.keys()]
        values = tuple(row_habit_obj.values()) + (habit_id,)
        # values,placeholders,columns=makeHabitRegeistingObject()
        sql=f'UPDATE habit SET {', '.join(habit_columns)} WHERE id=?'
        db.execute(sql,values)
        db.commit()
      
      elif action=="delete":
        db.execute(
          f'DELETE FROM habit WHERE id=?',(habit_id,)
        )
        db.commit()
        print("delete")
        return redirect(url_for('habits.list'))
    
    # GET
    habit_obj=db.execute(
      'SELECT * FROM habit WHERE id=(?)',(habit_id,)
    ).fetchone()
    # print(dict(habit_obj))
    return render_template(
      'habits/edit.html',
      habit_obj=habit_obj
    )
  
  except Exception as e:
    return str(e)