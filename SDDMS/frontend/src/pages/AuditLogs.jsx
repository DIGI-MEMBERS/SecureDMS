import { useState } from "react";

function AuditLogs() {
  // Temporary mock data.
  // This will be replaced with backend data later.
  const [logs] = useState([
    {
      user: "Officer A",
      action: "Uploaded document",
      time: "10:42 AM",
      status: "Success",
    },
    {
      user: "Officer B",
      action: "Viewed document",
      time: "10:45 AM",
      status: "Success",
    },
    {
      user: "Officer A",
      action: "Downloaded document",
      time: "11:02 AM",
      status: "Success",
    },
    {
      user: "Unauthorized User",
      action: "Access denied",
      time: "11:08 AM",
      status: "Denied",
    },
  ]);

  return (
    <div className="audit-logs-page">
      <div className="audit-logs-header">
        <div>
          <h1>Audit Logs</h1>

          <p>
            Monitor and review security-related activities.
          </p>
        </div>
      </div>

      <div className="audit-summary">
        <div className="audit-summary-card">
          <span>Total Activities</span>
          <strong>{logs.length}</strong>
        </div>

        <div className="audit-summary-card">
          <span>Successful Actions</span>
          <strong>
            {logs.filter((log) => log.status === "Success").length}
          </strong>
        </div>

        <div className="audit-summary-card">
          <span>Denied Actions</span>
          <strong>
            {logs.filter((log) => log.status === "Denied").length}
          </strong>
        </div>
      </div>

      <div className="audit-logs-container">
        <table className="audit-logs-table">
          <thead>
            <tr>
              <th>User</th>
              <th>Action</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {logs.map((log, index) => (
              <tr key={index}>
                <td>
                  <strong>{log.user}</strong>
                </td>

                <td>{log.action}</td>

                <td>{log.time}</td>

                <td>
                  <span
                    className={
                      log.status === "Denied"
                        ? "audit-status denied"
                        : "audit-status success"
                    }
                  >
                    {log.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AuditLogs;