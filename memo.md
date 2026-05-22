flaskr/__init__のSECRET='dev'の部分は、デプロイする際は変更する

flask --app flaskr --debug run
flask --app flaskr init-db

uv run -m
python -m

スキーマの変更とそれに伴うhabit.pyの変更を行った。
today.pyの変更が終了していないため、そちらの変更を次に行う。
また、delete機能がないため、追加する