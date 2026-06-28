function HealthItem({ title, value, color }) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "18px",
        paddingBottom: "10px",
        borderBottom: "1px solid #374151",
      }}
    >
      <span>{title}</span>

      <span
        style={{
          color,
          fontWeight: "bold",
          fontSize: "18px",
        }}
      >
        {value}
      </span>
    </div>
  );
}

function SupplyChainHealth({ data }) {

  if (!data) {
    return (
      <div
        style={{
          background: "#111827",
          padding: "24px",
          borderRadius: "18px",
        }}
      >
        <h2>Supply Chain Health</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div
      style={{
        background: "#111827",
        padding: "24px",
        borderRadius: "18px",
        boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
      }}
    >
      <h2>Supply Chain Health</h2>

      <p
        style={{
          color: "#9CA3AF",
          marginBottom: "24px",
        }}
      >
        Live operational health indicators
      </p>

      <HealthItem
        title="Inventory Risk"
        value={`${data.recommendation.inventory_risk}%`}
        color="#EF4444"
      />

      <HealthItem
        title="Supplier Risk"
        value={`${data.recommendation.supplier_risk}%`}
        color="#F59E0B"
      />

      <HealthItem
        title="Forecast Uncertainty"
        value={`${data.recommendation.forecast_uncertainty}%`}
        color="#3B82F6"
      />

      <HealthItem
        title="Market Regime"
        value={data.decision.regime}
        color={
          data.decision.regime === "Stable"
            ? "#22C55E"
            : data.decision.regime === "Seasonal"
            ? "#EAB308"
            : data.decision.regime === "Transitional"
            ? "#F97316"
            : "#EF4444"
        }
      />
    </div>
  );
}

export default SupplyChainHealth;