import { useState, useEffect } from "react";
import { api } from "../api/client";
import "../App.css";

const STATUS_COLORS = {
  done: "#3d7ea6",
  no_count: "#cccccc",
  not_done: "#e08787",
};

function Dashboard() {
  const [actions, setActions] = useState([]);
  const [selectedActionId, setSelectedActionId] = useState(null);
  const [stats, setStats] = useState(null);

  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("created_at");
  const [order, setOrder] = useState("desc");

  const [loadingActions, setLoadingActions] = useState(true);
  const [loadingStats, setLoadingStats] = useState(false);
  const [error, setError] = useState(null);

  // Action一覧を取得(検索・並び替えが変わるたびに再取得)
  useEffect(() => {
    fetchActions();
  }, [sort, order]);

  // 選択中のActionが変わったら、そのグラフデータを取得
  useEffect(() => {
    if (selectedActionId) {
      fetchStats(selectedActionId);
    }
  }, [selectedActionId]);

  async function fetchActions() {
    setLoadingActions(true);
    setError(null);
    try {
      const query = new URLSearchParams({
        sort,
        order,
        search,
        include_inactive: "true",
      }).toString();
      const data = await api.get(`/actions?${query}`);
      setActions(data);

      // まだ何も選択していなければ、一覧の先頭を自動選択する
      if (!selectedActionId && data.length > 0) {
        setSelectedActionId(data[0].id);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingActions(false);
    }
  }

  async function fetchStats(actionId) {
    setLoadingStats(true);
    setError(null);
    try {
      const data = await api.get(`/actions/${actionId}/stats`);
      setStats(data);
      console.log(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingStats(false);
    }
  }

  function handleSearchSubmit(e) {
    e.preventDefault();
    fetchActions();
  }

  return (
    <div>
      <h1>Dashboard</h1>

      {error && <p style={{ color: "red" }}>エラー: {error}</p>}

      <div style={{ display: "flex", gap: "32px" }}>
        {/* 左側:グラフ */}
        <div style={{ flex: 1 }}>
          {stats && (
            <div style={{ marginBottom: "8px" }} className="cardComponent">
              {stats.title}
            </div>
          )}

          <div
            style={{
              border: "1px solid #000",
              borderRadius: "16px",
              padding: "24px",
              display: "flex",
              alignItems: "flex-end",
              gap: "3px",
              height: "260px",
            }}
          >
            {loadingStats && <p>読み込み中...</p>}

            {!loadingStats &&
              stats &&
              stats.daily_stats.map((day) => (
                <div
                  key={day.date}
                  title={`${day.date}: ${day.status ?? "記録なし"}`}
                  style={{
                    flex: 1,
                    height: day.status ? "100%" : "20%",
                    backgroundColor: day.status
                      ? STATUS_COLORS[day.status]
                      : "#f0f0f0",
                    borderRadius: "4px",
                  }}
                />
              ))}
          </div>

          {stats && (
            <p style={{ marginTop: "12px" }}>
              直近30日: 達成 {stats.summary.done} / ノーカウント{" "}
              {stats.summary.no_count} / 未達成 {stats.summary.not_done} /
              記録なし {stats.summary.no_record}
            </p>
          )}
        </div>

        {/* 右側:Action一覧 */}
        <div style={{ flex: 1 }}>
          <form
            onSubmit={handleSearchSubmit}
            style={{ display: "flex", gap: "8px", marginBottom: "16px" }}
          >
            <select value={sort} onChange={(e) => setSort(e.target.value)}>
              <option value="created_at">作成日時順</option>
              <option value="title">タイトル順</option>
              <option value="updated_at">更新日時順</option>
            </select>
            <select value={order} onChange={(e) => setOrder(e.target.value)}>
              <option value="desc">降順</option>
              <option value="asc">昇順</option>
            </select>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="検索"
            />
            <button type="submit">検索</button>
          </form>

          {loadingActions ? (
            <p>読み込み中...</p>
          ) : actions.length === 0 ? (
            <p>登録されているActionがありません。</p>
          ) : (
            actions.map((action) => (
              <div
                key={action.id}
                className="cardComponent"
                onClick={() => setSelectedActionId(action.id)}
                style={{
                  borderColor:
                    action.id === selectedActionId ? "#3d7ea6" : "#000",
                  borderWidth: action.id === selectedActionId ? "2px" : "1px",
                }}
              >
                {action.title}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
