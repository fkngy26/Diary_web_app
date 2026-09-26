import { NavLink } from "react-router-dom";
import { navItems } from "./navItems";

function BottomNav() {
  return (
    <nav
      style={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        display: "flex",
        backgroundColor: "#cceeff",
        borderTop: "1px solid #99ccee",
        zIndex: 10,
      }}
    >
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          style={({ isActive }) => ({
            flex: 1,
            padding: "14px 0",
            textAlign: "center",
            textDecoration: "none",
            color: "#000",
            fontWeight: isActive ? "bold" : "normal",
          })}
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  );
}

export default BottomNav;
