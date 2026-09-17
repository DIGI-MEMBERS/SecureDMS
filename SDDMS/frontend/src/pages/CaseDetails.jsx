import { useParams } from "react-router-dom";

function CaseDetails() {
  const { id } = useParams();

  return (
    <div className="case-details-page">
      <div className="case-details-header">
        <div>
          <h1>Case #{id}</h1>
          <p>Case investigation details</p>
        </div>

        <span className="case-detail-status">
          Active
        </span>
      </div>

      <div className="case-info-card">
        <h2>Case Information</h2>

        <div className="case-info-grid">
          <div>
            <span>Case ID</span>
            <strong>#{id}</strong>
          </div>

          <div>
            <span>Case Title</span>
            <strong>Cyber Crime Investigation</strong>
          </div>

          <div>
            <span>Assigned Officer</span>
            <strong>Officer A</strong>
          </div>

          <div>
            <span>Department</span>
            <strong>Cyber Crime Division</strong>
          </div>

          <div>
            <span>Created Date</span>
            <strong>16 September 2026</strong>
          </div>

          <div>
            <span>Status</span>
            <strong>Active</strong>
          </div>
        </div>
      </div>

      <div className="case-info-card">
        <div className="documents-header">
          <div>
            <h2>Documents</h2>
            <p>Documents associated with this case</p>
          </div>

          <button className="create-case-button">
            + Upload Document
          </button>
        </div>

        <div className="document-placeholder">
          <p>📄 No documents loaded yet.</p>
          <small>
            Documents will be fetched from the backend.
          </small>
        </div>
      </div>
    </div>
  );
}

export default CaseDetails;