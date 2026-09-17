function EmptyState({
  title = "No data found",
  message = "There is nothing to display.",
}) {
  return (
    <div className="empty-state">
      <div className="empty-icon">📂</div>

      <h2>{title}</h2>

      <p>{message}</p>
    </div>
  );
}

export default EmptyState;