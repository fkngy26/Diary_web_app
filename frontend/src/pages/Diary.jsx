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

  const [memo, setMemo] = useState("");
  const [actionLogs, setActionLogs] = useState([]); // [{action_id, title, status}, ...]
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

    // status が未入力(null)のものは送らない
    const payload = {
      memo,
      action_logs: actionLogs
        .filter((log) => log.status)
        .map((log) => ({ action_id: log.action_id, status: log.status })),
    };

    try {
      await api.put(`/diaries/${date}`, payload);
      navigate("/diaries");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h1>Diary</h1>

      {error && <p style={{ color: "red" }}>エラー: {error}</p>}

      <p>{date}</p>

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
      </div>
    </div>
  );
}

export default Diary;
