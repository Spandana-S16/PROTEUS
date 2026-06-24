function MetricCard({ title, value }) {
  return (
    <div
      style={{
        background: "#111827",
        padding: "24px",
        borderRadius: "16px",
        minHeight: "120px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
      }}
    >
      <h3
        style={{
          color: "#9CA3AF",
          marginBottom: "12px",
          fontSize: "14px",
        }}
      >
        {title}
      </h3>

      <h1
        style={{
          fontSize: "32px",
        }}
      >
        {value}
      </h1>
    </div>
  );
}

export default MetricCard;