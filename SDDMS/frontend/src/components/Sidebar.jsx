import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Sidebar() {
  const { role } = useAuth();

  const menuItems = {
    "Investigating Officer": [
      {
        label: "Dashboard",
        path: "/dashboard",
      },
      {
        label: "Cases",
        path: "/cases",
      },
      {
        label: "Documents",
        path: "/documents",
      },
      {
        label: "Audit Logs",
        path: "/audit-logs",
      },
    ],

    "Forensic Officer": [
      {
        label: "Dashboard",
        path: "/dashboard",
      },
      {
        label: "Cases",
        path: "/cases",
      },
      {
        label: "Documents",
        path: "/documents",
      },
    ],

    "Legal Officer": [
      {
        label: "Dashboard",
        path: "/dashboard",
      },
      {
        label: "Cases",
        path: "/cases",
      },
      {
        label: "Documents",
        path: "/documents",
      },
    ],

    Admin: [
      {
        label: "Dashboard",
        path: "/dashboard",
      },
      {
        label: "Cases",
        path: "/cases",
      },
      {
        label: "Documents",
        path: "/documents",
      },
      {
        label: "Audit Logs",
        path: "/audit-logs",
      },
    ],
  };

  const items = menuItems[role] || [];

  return (
    <aside className="sidebar">
      <div className="sidebar-title">
        SecureDMS
      </div>

      <div className="sidebar-role">
        {role}
      </div>

      <nav className="sidebar-menu">
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive
                ? "sidebar-link active"
                : "sidebar-link"
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;