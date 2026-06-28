function WeightBar({ label, value, color }) {
  return (
    <div style={{ marginBottom: "22px" }}>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "8px",
          fontWeight: "600",
        }}
      >
        <span>{label}</span>
        <span>{value.toFixed(2)}%</span>
      </div>

      <div
        style={{
          width: "100%",
          height: "12px",
          background: "#374151",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${value}%`,
            height: "100%",
            background: color,
            borderRadius: "10px",
            transition: "width 0.8s ease",
          }}
        />
      </div>

    </div>
  );
}

function ModelContribution({ weights }) {

  return (
    <div
      style={{
        background: "#111827",
        padding: "24px",
        borderRadius: "18px",
        boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
      }}
    >
      <h2 style={{ marginBottom: "8px" }}>
        Adaptive Model Weights
      </h2>

      <p
        style={{
          color: "#9CA3AF",
          marginBottom: "24px",
        }}
      >
        Dynamic contribution of each forecasting model.
      </p>

      {weights ? (
        <>
          <WeightBar
            label="Prophet"
            value={weights.Prophet}
            color="#3B82F6"
          />

          <WeightBar
            label="XGBoost"
            value={weights.XGBoost}
            color="#F59E0B"
          />

          <WeightBar
            label="LSTM"
            value={weights.LSTM}
            color="#22C55E"
          />
        </>
      ) : (
        <p>Loading adaptive weights...</p>
      )}
    </div>
  );
}

export default ModelContribution;