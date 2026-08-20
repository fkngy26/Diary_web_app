import { useEffect, useState } from "react";

function ActionEditor() {
  const [name, setName] = useState("");

  useEffect(() => {
    document.title = `こんにちは、${name}さん`;
  });

  return (
    <>
      <input value={name} onChange={(e) => setName(e.target.value)} />

      <p>こんにちは、{name}さん</p>
    </>
  );
}
export default ActionEditor;
