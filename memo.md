flaskr/__init__のSECRET='dev'の部分は、デプロイする際は変更する

flask --app flaskr --debug run
flask --app flaskr init-db

uv run -m
python -m

today.pyで入力した際に、すでに今日のデータが存在した場合、追加ではなくUPDATEもしくは、削除する機能を追加する必要がある
また、delete機能がないため、追加する