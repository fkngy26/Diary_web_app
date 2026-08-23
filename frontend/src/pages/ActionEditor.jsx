import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import "../App.css";

const INTERVAL_UNITS = [
  { value: "day", label: "日" },
  { value: "week", label: "週間" },
  { value: "month", label: "ヶ月" },
  { value: "year", label: "年" },
];

function ActionEditor() {
  const { actionId } = useParams();
  console.log(actionId);
  const navigate = useNavigate();
  const isEditMode = actionId !== undefined; // /actions/new の場合、actionIdはundefinedになる

  const [title, setTitle] = useState("");
  const [hasDeadline, setHasDeadline] = useState(false);
  const [deadlineDate, setDeadlineDate] = useState("");
  const [intervalValue, setIntervalValue] = useState(1);
  const [intervalUnit, setIntervalUnit] = useState("day");

  // 編集モードか新規作成モードがある
  const [loading, setLoading] = useState(isEditMode); // 編集モードのときだけ最初にローディングする
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEditMode) {
      fetchAction();
    }
  }, [actionId]);

  async function fetchAction() {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get(`/actions/${actionId}`);
      setTitle(data.title);
      setHasDeadline(!!data.has_deadline);
      setDeadlineDate(data.deadline_date || "");
      setIntervalValue(data.interval_value);
      setIntervalUnit(data.interval_unit);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    setError(null);

    const payload = {
      title,
      has_deadline: hasDeadline,
      deadline_date: hasDeadline ? deadlineDate : null,
      interval_value: Number(intervalValue),
      interval_unit: intervalUnit,
    };

    try {
      if (isEditMode) {
        await api.put(`/actions/${actionId}`, payload);
      } else {
        await api.post("/actions", payload);
      }
      navigate("/actions");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    const confirmed = window.confirm(`「${title}」を削除しますか?`);
    if (!confirmed) return;

    setSaving(true);
    setError(null);
    try {
      await api.delete(`/actions/${actionId}`);
      navigate("/actions");
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  }

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h1>ActionEditor</h1>

      {error && <p style={{ color: "red" }}>エラー: {error}</p>}

      <form onSubmit={handleSubmit} style={{ maxWidth: "400px" }}>
        <div style={{ marginBottom: "16px" }}>
          <label>題名</label>
          <br />
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="例)筋トレ"
            required
            style={{ width: "100%" }}
          />
        </div>

        <div style={{ marginBottom: "16px" }}>
          <label>
            <input
              type="checkbox"
              checked={hasDeadline}
              onChange={(e) => setHasDeadline(e.target.checked)}
            />{" "}
            期限
          </label>
          {hasDeadline && (
            <input
              type="date"
              value={deadlineDate}
              onChange={(e) => setDeadlineDate(e.target.value)}
              required
              style={{ display: "block", marginTop: "8px" }}
            />
          )}
        </div>

        <div style={{ marginBottom: "24px" }}>
          <label>間隔</label>
          <br />
          <input
            type="number"
            min="1"
            value={intervalValue}
            onChange={(e) => setIntervalValue(e.target.value)}
            style={{ width: "60px", marginRight: "8px" }}
          />
          <select
            value={intervalUnit}
            onChange={(e) => setIntervalUnit(e.target.value)}
          >
            {INTERVAL_UNITS.map((unit) => (
              <option key={unit.value} value={unit.value}>
                {unit.label}
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: "flex", gap: "8px" }}>
          <button type="submit" disabled={saving}>
            {isEditMode ? "更新" : "作成"}
          </button>

          <button
            type="button"
            onClick={() => navigate("/actions")}
            disabled={saving}
          >
            キャンセル
          </button>

          {isEditMode && (
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
      </form>
    </div>
  );
}

export default ActionEditor;
