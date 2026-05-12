import functools

from flask import(
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp=Blueprint('habits',__name__,url_prefix='/habits')

@bp.route('/edit',methods=['GET','POST'])
def edit():
  if request.method=="GET":
    pass
    # try:
      # pass
      
  # DBからSQLで抽出
  # habitに代入して、render_templateの引数として渡す。
  habits={'habit_name':'getup'}
  return render_template(
    'habits/edit.html',
    habits=habits
  )