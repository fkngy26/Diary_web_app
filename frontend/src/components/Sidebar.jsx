import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/diaries", label: "DiaryList" },
  { to: "/actions", label: "ActionList" },
];

function Sidebar() {
  return (
    <nav
      style={{
        width: "200px",
        backgroundColor: "#cceeff",
        padding: "24px 16px",
        height: "100vh",
      }}
    >
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          style={({ isActive }) => ({
            display: "block",
            marginBottom: "16px",
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

export default Sidebar;
