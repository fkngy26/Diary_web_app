from flask import Blueprint, jsonify, request
from database import get_db
import psycopg2

bp = Blueprint('diaries', __name__, url_prefix='/api/diaries')

ALLOWED_STATUS = ['done', 'no_count', 'not_done']


def row_to_dict(row):
    return dict(row)


# 一覧取得(DiaryList画面用)
@bp.route('', methods=['GET'])
def get_diaries():
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM diaries ORDER BY date DESC')
        rows=cur.fetchall()
    return jsonify([row_to_dict(row) for row in rows])


# 指定日の日記+ログを取得(Diary画面用)
@bp.route('/<date>', methods=['GET'])
def get_diary(date):
    db = get_db()

    with db.cursor() as cur:
        cur.execute('SELECT * FROM diaries WHERE date = %s', (date,))
        diary=cur.fetchone()

    diary_dict = row_to_dict(diary) if diary else {'date': date, 'memo': ''}

    # 1. 現在アクティブな全Action(記録の有無を問わず、入力対象として表示)
    with db.cursor() as cur:
        cur.execute('SELECT id, title FROM actions WHERE is_active = 1 ORDER BY created_at')
        active_actions = cur.fetchall()

    diary_id = diary['id'] if diary else None
    if diary_id:
        with db.cursor() as cur:
            cur.execute(
                    'SELECT action_id, status FROM diary_action_logs WHERE diary_id = %s', (diary_id,)
                )
            log_rows=cur.fetchall()
    else:
        log_rows=[]
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
    if diary_id:
        with db.cursor() as cur:
            cur.execute(
                '''
                SELECT actions.id AS action_id, actions.title, logs.status
                FROM diary_action_logs AS logs
                JOIN actions ON actions.id = logs.action_id
                WHERE logs.diary_id = %s AND actions.is_active = 0
                ''',
                (diary_id,)
            )
            archived_rows=cur.fetchall()
    else:
        archived_rows=[]

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
    with db.cursor() as cur:
        cur.execute('SELECT id FROM diaries WHERE date = %s', (date,))
        existing=cur.fetchone()

    try:
        if existing:
            with db.cursor() as cur:
                cur.execute(
                    'UPDATE diaries SET memo = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s',
                    (memo, existing['id'])
                )
                diary_id = existing['id']
        else:
            with db.cursor() as cur:
                cur.execute(
                    'INSERT INTO diaries (date, memo) VALUES (%s, %s) RETURNING id',
                    (date, memo)
                )
                diary_id = cur.fetchone()['id']
    except Exception as e:
        db.rollback()
        return jsonify({'error':'idらへんのエラー'}),400

    # ログは一旦全部消してから入れ直す(シンプルで確実な方法)
    with db.cursor() as cur:
        cur.execute('DELETE FROM diary_action_logs WHERE diary_id = %s', (diary_id,))

    for log in action_logs:
        with db.cursor() as cur:
            cur.execute(
                'INSERT INTO diary_action_logs (diary_id, action_id, status) VALUES (%s, %s, %s)',
                (diary_id, log['action_id'], log['status'])
            )

    db.commit()

    with db.cursor() as cur:
        cur.execute('SELECT * FROM diaries WHERE id = %s', (diary_id,))
        updated_row=cur.fetchone()

    return jsonify(row_to_dict(updated_row))

# 日付の変更
@bp.route('/<int:diary_id>/date', methods=['PATCH'])
def update_diary_date(diary_id):
    db = get_db()

    with db.cursor() as cur:
        cur.execute('SELECT * FROM diaries WHERE id = %s', (diary_id,))
        existing=cur.fetchone()

    if existing is None:
        return jsonify({'error': 'Diary not found'}), 404

    data = request.get_json()
    new_date = data.get('date')
    if not new_date:
        return jsonify({'error': 'date is required'}), 400

    try:
        with db.cursor() as cur:
            cur.execute(
                'UPDATE diaries SET date = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s',
                (new_date, diary_id)
            )
        db.commit()
    except psycopg2.errors.IntegrityError:
        db.rollback()
        return jsonify({'error': f'{new_date} の日記はすでに存在します'}), 409

    with db.cursor() as cur:
        cur.execute('SELECT * FROM diaries WHERE id = %s', (diary_id,))
        updated_row = cur.fetchone()
    return jsonify(row_to_dict(updated_row))


# 削除(物理削除)
@bp.route('/<date>', methods=['DELETE'])
def delete_diary(date):
    db = get_db()

    with db.cursor as cur:
        cur.execute('SELECT * FROM diaries WHERE date = %s', (date,))
        existing = cur.fetchone()
    if existing is None:
        return jsonify({'error': 'Diary not found'}), 404

    with db.cursor as cur:
        cur.execute('DELETE FROM diaries WHERE date = %s', (date,))
    db.commit()

    return jsonify({'message': 'deleted'}), 200