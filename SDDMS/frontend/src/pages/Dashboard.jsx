function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <h1>SecureDMS Dashboard</h1>
          <p>Secure Digital Document Management System</p>
        </div>

        <div className="user-info">
          <span>👤</span>
          <div>
            <strong>Officer</strong>
            <small>Investigating Officer</small>
          </div>
        </div>
      </div>

      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Cases</h3>
          <p>12</p>
        </div>

        <div className="stat-card">
          <h3>Documents</h3>
          <p>86</p>
        </div>

        <div className="stat-card">
          <h3>Pending Approvals</h3>
          <p>4</p>
        </div>

        <div className="stat-card">
          <h3>Security Alerts</h3>
          <p>2</p>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Quick Actions</h2>

        <div className="quick-actions">
          <button>View Cases</button>
          <button>View Documents</button>
          <button>Audit Logs</button>
          <button>Security Alerts</button>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Recent Activity</h2>

        <div className="activity-card">
          <p>
            📄 Document uploaded — Case #1024
          </p>

          <p>
            🔐 Document hash verified successfully
          </p>

          <p>
            👤 Officer accessed investigation record
          </p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;