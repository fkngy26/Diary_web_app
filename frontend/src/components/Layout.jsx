// import { Outlet } from "react-router-dom";
// import Sidebar from "./Sidebar";

// function Layout() {
//   return (
//     <div style={{ display: "flex" }}>
//       <Sidebar />
//       <main style={{ flex: 1, padding: "32px" }}>
//         <Outlet />
//       </main>
//     </div>
//   );
// }

// export default Layout;

import { useState } from "react";
import { Outlet } from "react-router-dom";
import { useMediaQuery } from "react-responsive";
import Sidebar from "./Sidebar";
import BottomNav from "./BottomNav";

function Layout() {
  const isMobile = useMediaQuery({ maxWidth: 767 });
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div style={{ display: "flex" }}>
      {/* PC: サイドバーを常に表示 */}
      {!isMobile && <Sidebar />}

      {/* スマホ: ボタンで開閉 */}
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
