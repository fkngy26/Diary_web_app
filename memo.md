flaskr/__init__のSECRET='dev'の部分は、デプロイする際は変更する

flask --app flaskr --debug run
flask --app flaskr init-db

schema.sqlを変更する必要あり
- 日記のDateをユニークにする必要がある
- タスクの自由度を上げるため項目を増やす

Habitのスキーマを変更する必要がある
また、サーバサイドの入力も変更する。

habit.pyのbutton-addが押されたときの分岐の追加を行う。
⇒edit.htmlの中身とスキーマが食い違っているので、修正の必要あり