import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import "../App.css";

function DiaryList() {
  const navigate = useNavigate();
  const [diaries, setDiaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDiaries();
  }, []);

  async function fetchDiaries() {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get("/diaries");
      setDiaries(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleNewClick() {
    // 今日の日付をYYYY-MM-DD形式で作り、その日のDiaryページに飛ぶ
    const today = new Date().toISOString().split("T")[0];
    navigate(`/diaries/${today}`);
  }

  if (loading) return <p>読み込み中...</p>;
  if (error) return <p style={{ color: "red" }}>エラー: {error}</p>;

  return (
    <div>
      <h1>DiaryList</h1>

      <div className="cardComponent" onClick={handleNewClick}>
        New
      </div>

      {diaries.length === 0 ? (
        <p>まだ日記がありません。</p>
      ) : (
        diaries.map((diary) => (
          <div
            key={diary.id}
            className="cardComponent"
            onClick={() => navigate(`/diaries/${diary.date}`)}
          >
            {diary.date}
          </div>
        ))
      )}
    </div>
  );
}

export default DiaryList;
