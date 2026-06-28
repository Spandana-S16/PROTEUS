import { useState } from "react";

function ScenarioSimulator() {
  const [scenario, setScenario] = useState("normal");

  const scenarioData = {
    normal: {
      resilience: 88,
      regime: "Stable",
      forecast: "89,216 Units",
      confidence: "91%",
      color: "#22C55E",
      description:
        "Normal operating conditions. Demand is stable and the supply chain is performing efficiently.",
      recommendations: [
        "Maintain current inventory",
        "Continue supplier allocation",
        "Review forecasts weekly",
      ],
    },

    covid: {
      resilience: 38,
      regime: "Disrupted",
      forecast: "64,285 Units",
      confidence: "43%",
      color: "#EF4444",
      description:
        "Pandemic shock detected. Demand volatility has increased significantly and logistics delays are expected.",
      recommendations: [
        "Increase safety stock",
        "Activate contingency suppliers",
        "Review forecasts daily",
      ],
    },

    suez: {
      resilience: 55,
      regime: "Logistics Disruption",
      forecast: "71,904 Units",
      confidence: "61%",
      color: "#F59E0B",
      description:
        "Major shipping disruption detected. International lead times may increase considerably.",
      recommendations: [
        "Diversify shipping routes",
        "Increase inventory buffers",
        "Monitor supplier deliveries",
      ],
    },

    supplier: {
      resilience: 49,
      regime: "Supplier Failure",
      forecast: "68,745 Units",
      confidence: "58%",
      color: "#F97316",
      description:
        "Primary supplier unavailable. Backup suppliers should be activated immediately.",
      recommendations: [
        "Switch to backup suppliers",
        "Prioritize critical inventory",
        "Reduce non-essential demand",
      ],
    },

    surge: {
      resilience: 73,
      regime: "Demand Surge",
      forecast: "104,820 Units",
      confidence: "79%",
      color: "#3B82F6",
      description:
        "Demand spike detected. Inventory replenishment should be accelerated to avoid stockouts.",
      recommendations: [
        "Increase replenishment",
        "Expand warehouse capacity",
        "Monitor demand every day",
      ],
    },
  };

  const current = scenarioData[scenario];

  return (
    <div
      style={{
        background: "#111827",
        padding: "24px",
        borderRadius: "18px",
        marginTop: "30px",
        boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
      }}
    >
      <h2>Scenario Simulator</h2>

      <p
        style={{
          color: "#9CA3AF",
          marginBottom: "20px",
        }}
      >
        Simulate different supply chain disruptions.
      </p>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "12px",
          marginBottom: "25px",
        }}
      >
        <button onClick={() => setScenario("normal")}>Normal</button>

        <button onClick={() => setScenario("covid")}>
          Pandemic
        </button>

        <button onClick={() => setScenario("suez")}>
          Logistics
        </button>

        <button onClick={() => setScenario("supplier")}>
          Supplier Failure
        </button>

        <button onClick={() => setScenario("surge")}>
          Demand Surge
        </button>
      </div>

      <div
        style={{
          background: "#1F2937",
          borderRadius: "14px",
          padding: "20px",
        }}
      >
        <h2
          style={{
            color: current.color,
            marginBottom: "10px",
          }}
        >
          {current.regime}
        </h2>

        <p
          style={{
            color: "#D1D5DB",
            lineHeight: "1.7",
          }}
        >
          {current.description}
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3,1fr)",
            gap: "20px",
            marginTop: "25px",
          }}
        >
          <div>
            <h4 style={{ color: "#9CA3AF" }}>
              Resilience
            </h4>

            <h2>{current.resilience}/100</h2>
          </div>

          <div>
            <h4 style={{ color: "#9CA3AF" }}>
              Forecast
            </h4>

            <h2>{current.forecast}</h2>
          </div>

          <div>
            <h4 style={{ color: "#9CA3AF" }}>
              Confidence
            </h4>

            <h2>{current.confidence}</h2>
          </div>
        </div>

        <div
          style={{
            marginTop: "25px",
          }}
        >
          <h3>Recommended Actions</h3>

          <ul
            style={{
              marginTop: "10px",
              lineHeight: "2",
            }}
          >
            {current.recommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ScenarioSimulator;