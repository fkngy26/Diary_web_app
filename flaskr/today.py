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
  today_txt=str(datetime.datetime.today().date())
  try:
    if request.method=='POST':
      # チェックされたHabitを集計する
      checked_list=request.form.getlist('habit_ids')
      placeholder=', '.join(['?']*len(checked_list))
      checked_habit_obj=db.execute(
        f'SELECT * FROM habit WHERE id IN ({placeholder})',
        (checked_list)
      ).fetchall()
      regist_datas=[]
      for obj in checked_habit_obj:
        regist_data=[]
        regist_data.append(str(today_txt))
        # regist_data.append("2026-05-31")
        regist_data.append(obj['id'])
        regist_datas.append(regist_data)

      today_data=db.execute(
        f'SELECT * FROM habit_logs WHERE date=(?)',(str(today_txt),)
      ).fetchall()

      # 既に今日のタスクがあるならUPDATEに切り替える
      if today_data:
        for obj in regist_datas:
          obj.append(str(today_txt))
        db.executemany(
          f'UPDATE habit_logs SET date=?, habit_id=? WHERE date=?',regist_datas
        )
      else:
        db.executemany(
          f'INSERT INTO habit_logs ( date, habit_id) VALUES ( ?, ?)',
          regist_datas
        )
        

      # diary
      diary_text=request.form.get('diary')
      today_diary_indb=db.execute(
        f'SELECT * FROM diary WHERE date=?',(str(today_txt),)
      ).fetchone()

      if today_diary_indb:
        db.execute(
          "UPDATE diary SET date=?, diary_text=? WHERE date=?",(today_txt,diary_text,diary_text)
        )
      else:
        db.execute(
          "INSERT INTO diary ( date, diary_text) VALUES (?,?)",
          (today_txt,diary_text)
        )
      db.commit()

      # デバッグ用
      a=db.execute(
        'SELECT * FROM habit_logs'
      ).fetchall()
      print("-----Debug--------------------------")
      print("habit_logs")
      for b in a:
        print(dict(b))
      diaries=db.execute(
        "SELECT * FROM diary"
      ).fetchall()
      print("diary")
      for d in diaries:
        print(dict(d))

  # ==================================
  # 今日表示する必要があるHabitを抽出する。（未）
  # ==================================
    db_tasks=db.execute(
      'SELECT * FROM habit'
    ).fetchall()
    today_log=db.execute(
      'SELECT habit_id FROM habit_logs WHERE date == ?',
      [str(today_txt)]
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