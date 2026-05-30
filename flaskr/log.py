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
                "SELECT * FROM diary"
            ).fetchall()
            for i in logs:
                print(dict(i))
            return render_template(
                "log/logList.html",
                logs=logs
            )
        except Exception as e:
            return str(e)
    # return render_template("log/logList.html")

@bp.route('/<string:log_date>',methods=['GET','POST'])
def logPreview(log_date):
    if request.method=='POST':
        page_action=request.form.get['action']
        if page_action=='back':
            return redirect(url_for('log.logList'))
    
    # GET
    db=get_db()
    habit_logs=db.execute(
        'SELECT * FROM habit_logs WHERE date=?',(log_date,)
    ).fetchall()
    checked_habit_ids=[]
    for habit_log in habit_logs:
        checked_habit_ids.append(habit_log['habit_id'])
    try:
        print(checked_habit_ids)
        placeholders=', '.join(['?']*len(checked_habit_ids))
        preview_obj_name=db.execute(
            f'SELECT habit_name FROM habit WHERE id IN ({placeholders})',
            checked_habit_ids
        ).fetchall()
        for i in preview_obj_name:
            print(dict(i))
    except Exception as e:
        print(str(e))
        preview_obj_name=[
            {'habit_name':'NoRegist'}
        ]
        print("a")
        for i in preview_obj_name:
            print(dict(i))
        print("a")
    try:
        diary_log=db.execute(
            'SELECT diary_text FROM diary WHERE date=?',
            (log_date,)
        ).fetchone()
        print(dict(diary_log))
    except Exception as e:
        print(str(e))
        diary_log={
            'diary_text':'NoRegist'
        }
    return render_template(
        "log/logPreview.html",
        date=log_date,
        habits_log=preview_obj_name,
        diary_log=diary_log
    )