import { useParams } from "react-router-dom";
import { useState } from "react";

function VersionHistory() {
  const { id } = useParams();

  // Temporary mock data.
  // We will replace this with backend data later.
  const [versions] = useState([
    {
      version: "v3",
      fileName: "FIR_Report.pdf",
      uploadedBy: "Officer A",
      uploadedAt: "17 September 2026, 09:15 AM",
      status: "Current",
    },
    {
      version: "v2",
      fileName: "FIR_Report.pdf",
      uploadedBy: "Officer A",
      uploadedAt: "16 September 2026, 04:30 PM",
      status: "Previous",
    },
    {
      version: "v1",
      fileName: "FIR_Report.pdf",
      uploadedBy: "Officer B",
      uploadedAt: "16 September 2026, 11:20 AM",
      status: "Previous",
    },
  ]);

  return (
    <div className="version-history-page">
      <div className="version-history-header">
        <div>
          <h1>Version History</h1>
          <p>
            View the previous versions of document #{id}.
          </p>
        </div>
      </div>

      <div className="version-document-card">
        <div>
          <span>Document</span>
          <strong>FIR_Report.pdf</strong>
        </div>

        <div>
          <span>Document ID</span>
          <strong>{id}</strong>
        </div>

        <div>
          <span>Total Versions</span>
          <strong>{versions.length}</strong>
        </div>
      </div>

      <div className="versions-table-container">
        <table className="versions-table">
          <thead>
            <tr>
              <th>Version</th>
              <th>File Name</th>
              <th>Uploaded By</th>
              <th>Date & Time</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {versions.map((version) => (
              <tr key={version.version}>
                <td>
                  <strong>{version.version}</strong>
                </td>

                <td>{version.fileName}</td>

                <td>{version.uploadedBy}</td>

                <td>{version.uploadedAt}</td>

                <td>
                  <span className="version-status">
                    {version.status}
                  </span>
                </td>

                <td>
                  <button className="view-version-button">
                    View
                  </button>

                  <button className="download-version-button">
                    Download
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default VersionHistory;