import { Outlet } from "react-router-dom";
import { useIsMobile } from "../hooks/useIsMobile";
import Sidebar from "./Sidebar";
import BottomNav from "./BottomNav";

function Layout() {
  const isMobile = useIsMobile();

  return (
    <div style={{ display: "flex" }}>
      {/* PC: サイドバーを常に表示 */}
      {!isMobile && <Sidebar />}

      {/* スマホ: 下部ナビを表示 */}
      {isMobile && <BottomNav />}

      <main
        style={{
          flex: 1,
          padding: isMobile ? "56px 16px 16px" : "32px",
          minWidth: 0,
        }}
      >
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
