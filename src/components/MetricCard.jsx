function MetricCard({ title, value }) {

  let color = "#60A5FA";

  if (title === "Resilience Score") {

    const score = parseFloat(value);

    if (score >= 75) {
      color = "#22C55E";
    } else if (score >= 40) {
      color = "#F59E0B";
    } else {
      color = "#EF4444";
    }

  } else if (title === "Forecast reliability") {

    const score = parseFloat(value);

    if (score >= 70) {
      color = "#22C55E";
    } else if (score >= 40) {
      color = "#F59E0B";
    } else {
      color = "#EF4444";
    }

  } else {

    switch (value) {

      case "Stable":
      case "Excellent":
        color = "#22C55E";
        break;

      case "Seasonal":
      case "Moderate":
        color = "#F59E0B";
        break;

      case "Transitional":
        color = "#F97316";
        break;

      case "Disrupted":
      case "High":
        color = "#EF4444";
        break;

      default:
        color = "#60A5FA";
    }
  }

  return (
  <div
    style={{
      background: "#111827",
      padding: "24px",
      borderRadius: "18px",
      minHeight: "130px",
      boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
      borderLeft: `6px solid ${color}`,
      transition: "0.3s",
    }}
  >
    <p
      style={{
        color: "#9CA3AF",
        fontSize: "15px",
        marginBottom: "18px",
        fontWeight: 600,
        textTransform: "uppercase",
        letterSpacing: "1px",
      }}
    >
      {title}
    </p>

    <h1
      style={{
        fontSize: "38px",
        margin: 0,
        color: "white",
        fontWeight: "700",
      }}
    >
      {value}
    </h1>

    <div
      style={{
        marginTop: "16px",
        width: "45px",
        height: "5px",
        background: color,
        borderRadius: "10px",
      }}
    />
  </div>
);
}

export default MetricCard;