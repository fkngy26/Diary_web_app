DROP TABLE IF EXISTS diary_action_logs;
DROP TABLE IF EXISTS diaries;
DROP TABLE IF EXISTS actions;

CREATE TABLE actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    has_deadline BOOLEAN NOT NULL DEFAULT 0,
    deadline_date DATE,
    interval_value INTEGER NOT NULL DEFAULT 1,
    interval_unit TEXT NOT NULL DEFAULT 'day' CHECK (interval_unit IN ('day', 'week', 'month', 'year')),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    memo TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diary_action_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diary_id INTEGER NOT NULL,
    action_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('done', 'no_count', 'not_done')),
    FOREIGN KEY (diary_id) REFERENCES diaries (id) ON DELETE CASCADE,
    FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE,
    UNIQUE (diary_id, action_id)
);