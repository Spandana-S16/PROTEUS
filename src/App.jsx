import { useEffect, useState } from "react";

import MetricCard from "./components/MetricCard";
import ForecastChart from "./components/ForecastChart";
import ModelContribution from "./components/ModelContribution";
import SupplyChainHealth from "./components/SupplyChainHealth";
import ScenarioSimulator from "./components/ScenarioSimulator";

function App() {

  const [backendData, setBackendData] = useState(null);

  useEffect(() => {

    fetch("http://127.0.0.1:5000/forecast")
      .then((res) => res.json())
      .then((data) => {

        console.log(data);

        setBackendData(data);

      })
      .catch((err) => console.error(err));

  }, []);

  return (
    <div
      style={{
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "40px",
        background: "#0F172A",
        minHeight: "100vh",
        color: "white",
        fontFamily: "Inter, sans-serif",
      }}
    >
      <h1
        style={{
          fontSize: "42px",
          marginBottom: "10px",
        }}
      >
        PROTEUS
      </h1>

      <p
        style={{
          color: "#9CA3AF",
          marginBottom: "40px",
          fontSize: "18px",
        }}
      >
        Adaptive Supply Chain Intelligence Platform
      </p>

      {/* Top Metrics */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
        }}
      >
        <MetricCard
          title="Resilience Score"
          value={
            backendData
              ? backendData.stability.overall.score.toFixed(2)
              : "Loading..."
          }
        />

        <MetricCard
          title="Demand Regime"
          value={
            backendData
              ? backendData.decision.regime
              : "Loading..."
          }
        />

        <MetricCard
          title="Forecast"
          value={
            backendData
              ? backendData.fusion.forecast.toLocaleString()
              : "Loading..."
          }
        />

        <MetricCard
          title="Confidence"
          value={
            backendData
              ? backendData.fusion.ensemble_confidence.toFixed(2) + "%"
              : "Loading..."
          }
        />
      </div>

      <ForecastChart
        forecast={backendData?.fusion?.forecast}
      />

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          marginTop: "25px",
        }}
      >
        <ModelContribution
          weights={backendData?.fusion?.weights}
        />

        <SupplyChainHealth 
          data={backendData}
        />
      </div>

      <ScenarioSimulator />

      <div
  style={{
    background: "#111827",
    marginTop: "30px",
    padding: "30px",
    borderRadius: "18px",
    boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
    maxHeight: "420px",
    overflowY: "auto",
  }}
>
        <h2
          style={{
            marginBottom: "15px",
          }}
        >
          🧠 AI Executive Report
        </h2>

        <p
          style={{
            color: "#D1D5DB",
            lineHeight: "1.8",
            whiteSpace: "pre-wrap",
          }}
        >
          {backendData
            ? backendData["ai executive report"]
            :<div>
  <h3> Running Adaptive Fusion...</h3>

  <p>✓ Stability Analysis</p>
  <p>✓ Regime Detection</p>
  <p>✓ Forecast Generation</p>
  <p>✓ AI Executive Report</p>
</div>}
        </p>
      </div>
    </div>
  );
}

export default App;