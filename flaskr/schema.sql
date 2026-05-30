DROP TABLE IF EXISTS diary;
DROP TABLE IF EXISTS habit;
DROP TABLE IF EXISTS habit_logs;
DROP TABLE IF EXISTS deleted_habit;

CREATE TABLE diary (
  date TEXT NOT NULL PRIMARY KEY,
  diary_text TEXT
);
CREATE TABLE habit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  habit_name TEXT NOT NULL,
  repeat_interval INTEGER NOt NULL DEFAULT 1,
  is_end INTEGER NOT NULL DEFAULT 0,
  end_date TEXT,
  start_date TEXT NOT NULL
);
CREATE TABLE habit_logs (
  date TEXT NOT NULL,
  habit_id INTEGER NOT NULL,
  PRIMARY KEY (date,habit_id),
  FOREIGN KEY(habit_id) REFERENCES habit(id)
);