import { useState } from "react";

function Documents() {
  const [documents] = useState([
    {
      id: "DOC-001",
      name: "FIR_Report.pdf",
      type: "PDF",
      size: "2.4 MB",
      status: "Verified",
    },
    {
      id: "DOC-002",
      name: "Evidence_Report.pdf",
      type: "PDF",
      size: "4.8 MB",
      status: "Verified",
    },
    {
      id: "DOC-003",
      name: "Witness_Statement.pdf",
      type: "PDF",
      size: "1.7 MB",
      status: "Verified",
    },
  ]);

  return (
    <div className="documents-page">
      <div className="documents-page-header">
        <div>
          <h1>Documents</h1>
          <p>Securely manage case-related documents.</p>
        </div>

        <button className="upload-button">
          + Upload Document
        </button>
      </div>

      <div className="documents-table-container">
        <table className="documents-table">
          <thead>
            <tr>
              <th>Document ID</th>
              <th>Document Name</th>
              <th>Type</th>
              <th>Size</th>
              <th>Security Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {documents.map((document) => (
              <tr key={document.id}>
                <td>{document.id}</td>
                <td>{document.name}</td>
                <td>{document.type}</td>
                <td>{document.size}</td>
                <td>
                  <span className="document-status">
                    🔐 {document.status}
                  </span>
                </td>
                <td>
                  <button className="view-document-button">
                    View
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

export default Documents;