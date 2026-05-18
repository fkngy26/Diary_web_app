flaskr/__init__のSECRET='dev'の部分は、デプロイする際は変更する

flask --app flaskr --debug run
flask --app flaskr init-db

schema.sqlを変更する必要あり
- 日記のDateをユニークにする必要がある
- タスクの自由度を上げるため項目を増やす

タスクの登録画面を作成中（edit.html）