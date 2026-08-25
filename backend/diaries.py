from flask import Blueprint, jsonify, request
from database import get_db
import sqlite3

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

    diary = db.execute('SELECT * FROM diaries WHERE date = ?', (date,)).fetchone()
    diary_dict = row_to_dict(diary) if diary else {'date': date, 'memo': ''}

    # 1. 現在アクティブな全Action(記録の有無を問わず、入力対象として表示)
    active_actions = db.execute(
        'SELECT id, title FROM actions WHERE is_active = 1 ORDER BY created_at'
    ).fetchall()

    diary_id = diary['id'] if diary else None
    log_rows = db.execute(
        'SELECT action_id, status FROM diary_action_logs WHERE diary_id = ?', (diary_id,)
    ).fetchall() if diary_id else []
    status_by_action_id = {row['action_id']: row['status'] for row in log_rows}

    action_logs = [
        {
            'action_id': a['id'],
            'title': a['title'],
            'status': status_by_action_id.get(a['id']),
            'is_archived': 0,
        }
        for a in active_actions
    ]

    # 2. 記録は残っているが、対応するActionが非アクティブなもの(過去の記録として表示のみ)
    archived_rows = db.execute(
        '''
        SELECT actions.id AS action_id, actions.title, logs.status
        FROM diary_action_logs AS logs
        JOIN actions ON actions.id = logs.action_id
        WHERE logs.diary_id = ? AND actions.is_active = 0
        ''',
        (diary_id,)
    ).fetchall() if diary_id else []

    action_logs += [
        {
            'action_id': row['action_id'],
            'title': row['title'],
            'status': row['status'],
            'is_archived': 1,
        }
        for row in archived_rows
    ]

    diary_dict['action_logs'] = action_logs
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

    updated_row = db.execute('SELECT * FROM diaries WHERE id = ?', (diary_id,)).fetchone()
    return jsonify(row_to_dict(updated_row))

# 日付の変更
@bp.route('/<int:diary_id>/date', methods=['PATCH'])
def update_diary_date(diary_id):
    db = get_db()

    existing = db.execute('SELECT * FROM diaries WHERE id = ?', (diary_id,)).fetchone()
    if existing is None:
        return jsonify({'error': 'Diary not found'}), 404

    data = request.get_json()
    new_date = data.get('date')
    if not new_date:
        return jsonify({'error': 'date is required'}), 400

    try:
        db.execute(
            'UPDATE diaries SET date = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (new_date, diary_id)
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': f'{new_date} の日記はすでに存在します'}), 409

    updated_row = db.execute('SELECT * FROM diaries WHERE id = ?', (diary_id,)).fetchone()
    return jsonify(row_to_dict(updated_row))


# 削除(物理削除)
@bp.route('/<date>', methods=['DELETE'])
def delete_diary(date):
    db = get_db()

    existing = db.execute('SELECT * FROM diaries WHERE date = ?', (date,)).fetchone()
    if existing is None:
        return jsonify({'error': 'Diary not found'}), 404

    db.execute('DELETE FROM diaries WHERE date = ?', (date,))
    db.commit()

    return jsonify({'message': 'deleted'}), 200