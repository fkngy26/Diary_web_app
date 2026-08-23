import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import "../App.css";

function ActionList() {
  const navigate = useNavigate();

  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("created_at");
  const [order, setOrder] = useState("desc");

  useEffect(() => {
    fetchActions();
  }, [sort, order]); // sort・orderが変わるたびに再取得する

  async function fetchActions() {
    setLoading(true);
    setError(null);
    try {
      const query = new URLSearchParams({ sort, order, search }).toString();
      // console.log(query);
      const data = await api.get(`/actions?${query}`);
      setActions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // ここから
  function handleSearchSubmit(e) {
    e.preventDefault();
    fetchActions();
  }

  if (loading) return <p>読み込み中...</p>;
  if (error) return <p style={{ color: "red" }}>エラー: {error}</p>;

  return (
    <div>
      <h1>ActionList</h1>

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

      <button
        onClick={() => navigate("/actions/new")}
        style={{ marginBottom: "16px" }}
      >
        + 新規作成
      </button>

      {actions.length === 0 ? (
        <p>登録されているActionがありません。</p>
      ) : (
        actions.map((action) => (
          <div
            key={action.id}
            className="cardComponent"
            onClick={() => navigate(`/actions/${action.id}`)}
          >
            {action.title}
          </div>
        ))
      )}
    </div>
  );
}

export default ActionList;
