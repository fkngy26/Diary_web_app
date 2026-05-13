flaskr/__init__のSECRET='dev'の部分は、デプロイする際は変更する

today.pyのDBに入れる部分を書いた
      db.executemany(
        "INSERT INTO habit_logs (id, habit_id, date) VALUES (?,?,?)",
          task_objects
      )