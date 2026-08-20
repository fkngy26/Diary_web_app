from flask import Blueprint, jsonify, request
from database import get_db

bp = Blueprint('diaries', __name__, url_prefix='/api/diaries')

ALLOWED_STATUS = ['done', 'no_count', 'not_done']


def row_to_dict(row):
    return dict(row)


# 一覧取得(DiaryList画面用)
@bp.route('', methods=['GET'])
def get_diaries():
    db = get_db()
    rows = db.execute(
        'SELECT * FROM diaries ORDER BY date DESC'
    ).fetchall()
    return jsonify([row_to_dict(row) for row in rows])


# 指定日の日記+ログを取得(Diary画面用)
@bp.route('/<date>', methods=['GET'])
def get_diary(date):
    db = get_db()

    diary = db.execute(
        'SELECT * FROM diaries WHERE date = ?', (date,)
    ).fetchone()

    # その日の記録がまだ無い場合、日記は空として扱う
    diary_dict = row_to_dict(diary) if diary else {'date': date, 'memo': ''}

    # 有効なActionと、その日のログを紐付けて取得する
    logs = db.execute(
        '''
        SELECT actions.id AS action_id, actions.title, logs.status
        FROM actions
        LEFT JOIN diary_action_logs AS logs
            ON logs.action_id = actions.id
            AND logs.diary_id = (SELECT id FROM diaries WHERE date = ?)
        WHERE actions.is_active = 1
        ORDER BY actions.created_at
        ''',
        (date,)
    ).fetchall()

    diary_dict['action_logs'] = [row_to_dict(row) for row in logs]

    return jsonify(diary_dict)


# 指定日の日記+ログをまとめて保存(作成/更新をここで兼ねる)
@bp.route('/<date>', methods=['PUT'])
def upsert_diary(date):
    data = request.get_json()
    memo = data.get('memo', '')
    action_logs = data.get('action_logs', [])  # [{action_id: 1, status: 'done'}, ...]

    # ステータスの値チェック
    for log in action_logs:
        if log.get('status') not in ALLOWED_STATUS:
            return jsonify({'error': f'invalid status: {log.get("status")}'}), 400

    db = get_db()

    # 既存の日記を確認
    existing = db.execute('SELECT id FROM diaries WHERE date = ?', (date,)).fetchone()

    if existing:
        db.execute(
            'UPDATE diaries SET memo = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (memo, existing['id'])
        )
        diary_id = existing['id']
    else:
        cur = db.execute(
            'INSERT INTO diaries (date, memo) VALUES (?, ?)',
            (date, memo)
        )
        diary_id = cur.lastrowid

    # ログは一旦全部消してから入れ直す(シンプルで確実な方法)
    db.execute('DELETE FROM diary_action_logs WHERE diary_id = ?', (diary_id,))
    for log in action_logs:
        db.execute(
            'INSERT INTO diary_action_logs (diary_id, action_id, status) VALUES (?, ?, ?)',
            (diary_id, log['action_id'], log['status'])
        )

    db.commit()

    return jsonify({'message': 'saved', 'diary_id': diary_id})