import { useState } from "react";

function UploadDocument() {
  const [caseId, setCaseId] = useState("");
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleFileChange = (event) => {
    setError("");
    setSuccess("");

    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      setFile(null);
      return;
    }

    // Maximum file size: 10 MB
    const maxSize = 10 * 1024 * 1024;

    if (selectedFile.size > maxSize) {
      setError("File size must be less than 10 MB.");
      setFile(null);
      return;
    }

    // Allowed file types
    const allowedTypes = [
      "application/pdf",
      "image/jpeg",
      "image/png",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setError(
        "Invalid file type. Please upload PDF, JPG, PNG, DOC, or DOCX."
      );
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!caseId) {
      setError("Please select a case.");
      return;
    }

    if (!file) {
      setError("Please select a document.");
      return;
    }

    console.log("Case ID:", caseId);
    console.log("Selected file:", file);

    setSuccess(
      "File selected successfully. Backend upload will be connected next."
    );
  };

  return (
    <div className="upload-document-page">
      <div className="upload-document-card">
        <h1>Upload Document</h1>

        <p className="upload-description">
          Upload a document securely to an investigation case.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="case">
              Select Case
            </label>

            <select
              id="case"
              value={caseId}
              onChange={(event) => setCaseId(event.target.value)}
            >
              <option value="">Select a case</option>
              <option value="1024">
                #1024 - Cyber Crime Investigation
              </option>
              <option value="1025">
                #1025 - Financial Fraud Investigation
              </option>
              <option value="1026">
                #1026 - Theft Investigation
              </option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="document">
              Select Document
            </label>

            <input
              id="document"
              type="file"
              onChange={handleFileChange}
            />

            <small className="file-help">
              Allowed: PDF, JPG, PNG, DOC, DOCX | Maximum: 10 MB
            </small>
          </div>

          {file && (
            <div className="selected-file">
              <strong>Selected File:</strong>

              <p>{file.name}</p>

              <small>
                {(file.size / (1024 * 1024)).toFixed(2)} MB
              </small>
            </div>
          )}

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          {success && (
            <p className="success-message">
              {success}
            </p>
          )}

          <button type="submit" className="upload-submit-button">
            Upload Document
          </button>
        </form>
      </div>
    </div>
  );
}

export default UploadDocument;