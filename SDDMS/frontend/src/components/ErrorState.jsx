function ErrorState({
  statusCode,
  message,
  onRetry,
}) {
  let title = "Something went wrong";
  let defaultMessage = "Unable to complete the request.";

  if (statusCode === 401) {
    title = "Session Expired";
    defaultMessage = "Please login again to continue.";
  }

  if (statusCode === 403) {
    title = "Access Denied";
    defaultMessage =
      "You do not have permission to access this resource.";
  }

  if (statusCode === 404) {
    title = "Not Found";
    defaultMessage =
      "The requested resource could not be found.";
  }

  if (statusCode === 500) {
    title = "Server Error";
    defaultMessage =
      "Something went wrong on the server. Please try again later.";
  }

  if (statusCode === "NETWORK") {
    title = "Backend Unavailable";
    defaultMessage =
      "Unable to connect to the server. Please check your connection.";
  }

  return (
    <div className="error-state">
      <div className="error-icon">⚠️</div>

      <h2>{title}</h2>

      <p>{message || defaultMessage}</p>

      {onRetry && (
        <button
          className="retry-button"
          onClick={onRetry}
        >
          Try Again
        </button>
      )}
    </div>
  );
}

export default ErrorState;