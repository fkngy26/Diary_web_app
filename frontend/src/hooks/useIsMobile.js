import { useEffect, useState } from "react";

const QUERY = "(max-width: 767px)";

// react-responsive の代わりに、ブラウザ標準の matchMedia だけで判定するフック。
// 外部の依存パッケージを増やさないので、CommonJS の連鎖によるバンドルエラーを避けられる。
export function useIsMobile() {
  const [isMobile, setIsMobile] = useState(
    () => typeof window !== "undefined" && window.matchMedia(QUERY).matches,
  );

  useEffect(() => {
    const mql = window.matchMedia(QUERY);
    const handleChange = (e) => setIsMobile(e.matches);

    mql.addEventListener("change", handleChange);
    return () => mql.removeEventListener("change", handleChange);
  }, []);

  return isMobile;
}
