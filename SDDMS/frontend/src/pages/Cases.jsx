import { useEffect, useState } from "react";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import EmptyState from "../components/EmptyState";

function Cases() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const loadCases = () => {
    setLoading(true);
    setError(false);

    // Temporary simulation.
    // Real API will be connected later.
    setTimeout(() => {
      setCases([
        {
          id: "1024",
          title: "Cyber Crime Investigation",
          status: "Active",
          officer: "Officer A",
        },
        {
          id: "1025",
          title: "Financial Fraud Investigation",
          status: "Under Review",
          officer: "Officer B",
        },
        {
          id: "1026",
          title: "Theft Investigation",
          status: "Closed",
          officer: "Officer C",
        },
      ]);

      setLoading(false);
    }, 1000);
  };

  useEffect(() => {
    loadCases();
  }, []);

  if (loading) {
    return (
      <LoadingState message="Loading cases..." />
    );
  }

  if (error) {
    return (
      <ErrorState
        message="Unable to load cases. Please check your connection."
        onRetry={loadCases}
      />
    );
  }

  if (cases.length === 0) {
    return (
      <EmptyState
        title="No cases found"
        message="There are no investigation cases available."
      />
    );
  }

  return (
    <div className="cases-page">
      <div className="cases-header">
        <div>
          <h1>Cases</h1>

          <p>
            Manage and access investigation cases.
          </p>
        </div>

        <button className="create-case-button">
          + Create Case
        </button>
      </div>

      <div className="cases-table-container">
        <table className="cases-table">
          <thead>
            <tr>
              <th>Case ID</th>
              <th>Case Title</th>
              <th>Status</th>
              <th>Assigned Officer</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {cases.map((caseItem) => (
              <tr key={caseItem.id}>
                <td>#{caseItem.id}</td>

                <td>{caseItem.title}</td>

                <td>
                  <span className="case-status">
                    {caseItem.status}
                  </span>
                </td>

                <td>{caseItem.officer}</td>

                <td>
                  <button className="view-case-button">
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

export default Cases;