from flask import Blueprint, jsonify, request, g
from database import get_db
from datetime import timedelta, date
import sqlite3

bp = Blueprint('actions', __name__, url_prefix='/api/actions')

ALLOWED_SORT_COLUMNS = ['created_at', 'title', 'updated_at']
ALLOWED_INTERVAL_UNITS = ['day', 'week', 'month', 'year']

def row_to_dict(row):
    return dict(row)

@bp.route('/getall', methods=['GET'])
def get_all_actions():
    db = get_db()
    rows = db.execute('SELECT * FROM actions').fetchall()
    return jsonify([row_to_dict(row) for row in rows])

@bp.route('', methods=['GET'])
def get_actions():
    db = get_db()

    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    search = request.args.get('search', '')
    include_inactive = request.args.get('include_inactive', 'false') == 'true'

    if sort not in ALLOWED_SORT_COLUMNS:
        sort = 'created_at'
    order = 'ASC' if order.lower() == 'asc' else 'DESC'

    active_condition = '' if include_inactive else 'AND is_active = 1'

    query = f'''
        SELECT * FROM actions
        WHERE title LIKE ? {active_condition}
        ORDER BY {sort} {order}
    '''
    rows = db.execute(query, (f'%{search}%',)).fetchall()

    return jsonify([row_to_dict(row) for row in rows])


# 詳細取得(1件)
@bp.route('/<int:action_id>', methods=['GET'])
def get_action(action_id):
    db = get_db()
    row = db.execute(
        'SELECT * FROM actions WHERE id = ? AND is_active = 1',
        (action_id,)
    ).fetchone()

    if row is None:
        return jsonify({'error': 'Action not found'}), 404

    return jsonify(row_to_dict(row))


# 新規作成
@bp.route('', methods=['POST'])
def create_action():
    data = request.get_json()

    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'title is required'}), 400

    has_deadline = bool(data.get('has_deadline', False))
    deadline_date = data.get('deadline_date') if has_deadline else None
    interval_value = data.get('interval_value', 1)
    interval_unit = data.get('interval_unit', 'day')

    if interval_unit not in ALLOWED_INTERVAL_UNITS:
        return jsonify({'error': 'invalid interval_unit'}), 400

    db = get_db()
    cur = db.execute(
        '''
        INSERT INTO actions (title, has_deadline, deadline_date, interval_value, interval_unit)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (title, has_deadline, deadline_date, interval_value, interval_unit)
    )
    db.commit()

    new_row = db.execute('SELECT * FROM actions WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(new_row)), 201


# 更新
@bp.route('/<int:action_id>', methods=['PUT'])
def update_action(action_id):
    db = get_db()
    existing = db.execute('SELECT * FROM actions WHERE id = ? AND is_active = 1', (action_id,)).fetchone()
    if existing is None:
        return jsonify({'error': 'Action not found'}), 404

    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'title is required'}), 400

    has_deadline = bool(data.get('has_deadline', False))
    deadline_date = data.get('deadline_date') if has_deadline else None
    interval_value = data.get('interval_value', 1)
    interval_unit = data.get('interval_unit', 'day')

    if interval_unit not in ALLOWED_INTERVAL_UNITS:
        return jsonify({'error': 'invalid interval_unit'}), 400

    db.execute(
        '''
        UPDATE actions
        SET title = ?, has_deadline = ?, deadline_date = ?, interval_value = ?, interval_unit = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''',
        (title, has_deadline, deadline_date, interval_value, interval_unit, action_id)
    )
    db.commit()

    updated_row = db.execute('SELECT * FROM actions WHERE id = ?', (action_id,)).fetchone()
    return jsonify(row_to_dict(updated_row))


# 削除(論理削除)
@bp.route('/<int:action_id>', methods=['DELETE'])
def delete_action(action_id):
    db = get_db()
    existing = db.execute('SELECT * FROM actions WHERE id = ? AND is_active = 1', (action_id,)).fetchone()
    if existing is None:
        return jsonify({'error': 'Action not found'}), 404

    db.execute(
        'UPDATE actions SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (action_id,)
    )
    db.commit()

    return jsonify({'message': 'deleted'}), 200

# 全削除・リセット
@bp.route('',methods=['DELETE'])
def reset_action():
    try:
        db=get_db()
        db.execute(
                'DELETE FROM actions'
            )
        db.commit()
        return jsonify({'message': 'deleted'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'deleted'}), 500    

# 特定Actionの、直近1か月分の統計を取得
@bp.route('/<int:action_id>/stats', methods=['GET'])
def get_action_stats(action_id):
    db = get_db()

    print(action_id)
    action = db.execute(
        'SELECT * FROM actions WHERE id = ?', (action_id,)
    ).fetchone()
    if action is None:
        return jsonify({'error': 'Action not found'}), 404

    today = date.today()
    start_date = today - timedelta(days=29)  # 今日を含めて直近30日間

    rows = db.execute(
        '''
        SELECT diaries.date AS date, logs.status AS status
        FROM diaries
        JOIN diary_action_logs AS logs
            ON logs.diary_id = diaries.id AND logs.action_id = ?
        WHERE diaries.date >= ?
        ''',
        (action_id, start_date.isoformat())
    ).fetchall()

    # 日付をキーにした辞書に変換しておく(検索しやすくするため)
    status_by_date = {row['date']: row['status'] for row in rows}

    # 30日分、記録が無い日は status を null として埋める
    daily_stats = []
    for i in range(30):
        d = (start_date + timedelta(days=i)).isoformat()
        daily_stats.append({'date': d, 'status': status_by_date.get(d)})

    summary = {
        'done': sum(1 for s in daily_stats if s['status'] == 'done'),
        'no_count': sum(1 for s in daily_stats if s['status'] == 'no_count'),
        'not_done': sum(1 for s in daily_stats if s['status'] == 'not_done'),
        'no_record': sum(1 for s in daily_stats if s['status'] is None),
    }

    return jsonify({
        'action_id': action_id,
        'title': action['title'],
        'daily_stats': daily_stats,
        'summary': summary
    })