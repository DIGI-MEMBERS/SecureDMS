import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { role, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <strong>SecureDMS</strong>
      </div>

      <div className="navbar-user">
        <div className="navbar-user-info">
          <strong>Officer A</strong>
          <span>{role}</span>
        </div>

        <button
          className="logout-button"
          onClick={logout}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;