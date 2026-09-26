# 開発マニュアル

## 1. 全体構成

```
frontend (React + Vite)  ---/api--->  backend (Flask)  --->  PostgreSQL
```

- フロントは `frontend/src/api/client.js` で `BASE_URL = "/api"` という**相対パス**でリクエストしている。
- そのため「フロントとバックエンドが同じオリジン(同じドメイン)かどうか」で、動き方が変わる。

| 環境 | フロントの動き | `/api` の届き先 |
|---|---|---|
| 開発 (`npm run dev`) | Vite の開発サーバー(通常 `localhost:5173`)が動く | `frontend/vite.config.js` の `server.proxy` 設定により `http://localhost:5000`(Flask)へ転送 |
| 本番 (Render) | `npm run build` で作った `dist` を Flask 自身が配信 | フロントとバックエンドが同じオリジンなので、`proxy` なしでも直接 Flask に届く |

**重要**: `vite.config.js` の `server.proxy` は **開発時にしか使われない設定**で、`npm run build` の出力(`dist`)には含まれない。つまり、この部分は本番用に書き換える必要がなく、常に同じ内容のままでよい。

環境ごとに変える必要があるのは **`backend/.env` の `DATABASE_URL`** だけ(ローカルDB ⇄ Render上の外部DB)。`.env` は git 管理外なので、コードを書き換える必要はない。

## 2. 開発環境の起動手順

3つを別ターミナルで起動する。

```powershell
# 1. ローカルDB (Docker)
docker start diary-db

# 2. バックエンド (Flask, http://localhost:5000)
cd backend
uv run python app.py

# 3. フロントエンド (Vite, http://localhost:5173)
cd frontend
npm run dev
```

ブラウザは **`localhost:5173`** を開く(`5000` は `backend/dist` の古いビルドを返すだけなので開発中は使わない)。

### 初回だけ必要な準備
```powershell
cd frontend
npm install        # または npm ci
```
```powershell
cd backend
uv run flask --app app init-db   # DBのテーブルを作成(既存データは消えるので1回だけ)
```

## 3. 本番用ビルド & デプロイの流れ

```powershell
cd frontend
npm run build
```
`frontend/dist` の内容を `backend/dist` に入れ替えてからデプロイする。Render 側では `DATABASE_URL` を外部DBのものに設定しておく。

## 4. `git merge` 前後のチェックリスト

過去に、ブランチのマージで `vite.config.js` の設定(`server.proxy`)が意図せず消えたことがある。マージ後は、次のファイルが両方の変更を含んでいるか **`git diff`** で確認する。

```powershell
git diff HEAD~1 -- frontend/vite.config.js
```

特に確認するファイル:
- `frontend/vite.config.js` — `plugins`、`resolve.alias`、`server.proxy` がすべて残っているか
- `backend/app.py` — ルーティングや `init-db` コマンドが残っているか

目視だけでなく、**マージ直後に `npm run dev` で実際に画面とAPI通信の両方を確認する**(片方が動いていても、もう片方が壊れていることがあるため)。

## 5. トラブルシューティング

| 症状 | 疑う場所 |
|---|---|
| 画面が白紙・コンソールに `require` エラー | 依存パッケージのバージョンずれ([useIsMobile.js](frontend/src/hooks/useIsMobile.js) 参照。`react-responsive` は依存が多く不安定だったため削除済み) |
| 画面は出るがAPIレスポンスがJSONでない/HTMLが返る | `vite.config.js` の `server.proxy` が消えていないか確認 |
| DB接続エラー | `docker ps` でコンテナが起動しているか、`.env` の `DATABASE_URL` を確認 |
| `npm run dev` が認識されない | `frontend` で `npm install` 未実行 |

## 6. 今後の改善予定(memo.txt より)
- Dashboard の項目を示す部分を修正する
- スマホ版の作成
- ID とパスワードの入力
