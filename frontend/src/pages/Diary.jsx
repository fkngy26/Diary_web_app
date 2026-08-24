import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import "../App.css";

const STATUS_OPTIONS = [
  { value: "done", label: "○" },
  { value: "no_count", label: "−" },
  { value: "not_done", label: "×" },
];

function Diary() {
  const { date } = useParams();
  const navigate = useNavigate();

  const [diaryId, setDiaryId] = useState(null);
  const [editedDate, setEditedDate] = useState(date); // 編集用の日付(変更可能)
  const [memo, setMemo] = useState("");
  const [actionLogs, setActionLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDiary();
  }, [date]);

  async function fetchDiary() {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get(`/diaries/${date}`);
      setDiaryId(data.id || null); // まだ保存されていない日はidが無い
      setEditedDate(date);
      setMemo(data.memo || "");
      setActionLogs(data.action_logs || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleStatusChange(actionId, newStatus) {
    setActionLogs((prev) =>
      prev.map((log) =>
        log.action_id === actionId ? { ...log, status: newStatus } : log,
      ),
    );
  }

  async function handleSave() {
    setSaving(true);
    setError(null);

    const payload = {
      memo,
      action_logs: actionLogs
        .filter((log) => log.status)
        .map((log) => ({ action_id: log.action_id, status: log.status })),
    };

    try {
      // 1. まず現在のURLの日付(date)で内容を保存する
      const saved = await api.put(`/diaries/${date}`, payload);

      // 2. 日付が変更されていれば、続けて日付だけ変更するAPIを呼ぶ
      if (editedDate !== date) {
        await api.patch(`/diaries/${saved.id}/date`, { date: editedDate });
      }

      navigate("/diaries");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    const confirmed = window.confirm(`${date} の日記を削除しますか?`);
    if (!confirmed) return;

    setSaving(true);
    setError(null);
    try {
      await api.delete(`/diaries/${date}`);
      navigate("/diaries");
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  }

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h1>Diary</h1>

      {error && <p style={{ color: "red" }}>エラー: {error}</p>}

      <div style={{ marginBottom: "16px" }}>
        <label>日付</label>
        <br />
        <input
          type="date"
          value={editedDate}
          onChange={(e) => setEditedDate(e.target.value)}
        />
      </div>

      <div style={{ marginBottom: "24px" }}>
        {actionLogs.map((log) => (
          <div key={log.action_id} style={{ marginBottom: "8px" }}>
            <span style={{ marginRight: "12px" }}>{log.title}</span>
            {STATUS_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                type="button"
                onClick={() => handleStatusChange(log.action_id, opt.value)}
                style={{
                  fontWeight: log.status === opt.value ? "bold" : "normal",
                  backgroundColor:
                    log.status === opt.value ? "#cceeff" : "#fff",
                  marginRight: "4px",
                }}
              >
                {opt.label}
              </button>
            ))}
          </div>
        ))}
      </div>

      <div style={{ marginBottom: "16px" }}>
        <label>日記</label>
        <br />
        <textarea
          value={memo}
          onChange={(e) => setMemo(e.target.value)}
          rows={8}
          style={{ width: "100%" }}
        />
      </div>

      <div style={{ display: "flex", gap: "8px" }}>
        <button onClick={handleSave} disabled={saving}>
          保存
        </button>
        <button
          type="button"
          onClick={() => navigate("/diaries")}
          disabled={saving}
        >
          キャンセル
        </button>
        {diaryId && (
          <button
            type="button"
            onClick={handleDelete}
            disabled={saving}
            style={{ backgroundColor: "#ff8080", marginLeft: "auto" }}
          >
            削除
          </button>
        )}
      </div>
    </div>
  );
}

export default Diary;
