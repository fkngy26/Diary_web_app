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
  today=datetime.datetime.today().date()
  if request.method=='POST':
    try:
      # POSTでは、HabitとDiaryを保存する必要がある。
      # 既に登録されているものがある場合は、UPDATEする。

      # チェックされたHabitを集計する
      checked_list=request.form.getlist('habit_ids')
      placeholder=', '.join(['?']*len(checked_list))
      print(placeholder)
      checked_habit_obj=db.execute(
        f'SELECT * FROM habit WHERE id IN ({placeholder})',
        (checked_list)
      ).fetchall()
      regist_datas=[]
      for obj in checked_habit_obj:
        regist_data=[]
        regist_data.append(str(today))
        regist_data.append(obj['id'])
        regist_datas.append(regist_data)
      # ======================================
      # 消すやつ
      db.execute(
        'DELETE FROM habit_logs'
      )
      # ======================================
      db.executemany(
        f'INSERT INTO habit_logs ( date, habit_id) VALUES ( ?, ?)',
        regist_datas
      )
      # a=db.execute(
      #   'SELECT * FROM habit_logs'
      # ).fetchall()
      # for b in a:
      #   print(dict(b))

      diary_text=request.form.get('diary')
      print(diary_text)
      # ======================================
      # 消すやつ
      db.execute(
        'DELETE FROM diary'
      )
      # ======================================
      db.execute(
        "INSERT INTO diary ( date, diary_text) VALUES (?,?)",
        (today,diary_text)
      )
      db.commit()
      diaries=db.execute(
        "SELECT * FROM diary"
      ).fetchall()
      for d in diaries:
        print(dict(d))

    except Exception as e:
      print(str(e))

  try:
  # ==================================
  # 今日表示する必要があるHabitを抽出する。（未）
  # ==================================
    db_tasks=db.execute(
      'SELECT * FROM habit'
    ).fetchall()
    today_log=db.execute(
      'SELECT habit_id FROM habit_logs WHERE date == ?',
      [str(today)]
    ).fetchall()
    ids=[]
    for id in today_log:
      ids.append(id['habit_id'])
    return render_template(
      'today/writeTodayDiary.html',
      habits=db_tasks,
      checked_habits=ids
    )
  except Exception as e:
    return str(e)