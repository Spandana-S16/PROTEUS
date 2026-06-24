import MetricCard from "./components/MetricCard";
import ForecastChart from "./components/ForecastChart";
import ModelContribution from "./components/ModelContribution";
import SupplyChainHealth from "./components/SupplyChainHealth";

import {useState} from "react";
function App() {
  const [scenario, setScenario] = useState("normal");
  const scenarioData = {
  normal: {
    resilience: 88,
    regime: "Stable",
    forecast: 520,
    confidence: "91%",
  },

  covid: {
    resilience: 52,
    regime: "Volatile",
    forecast: 430,
    confidence: "68%",
  },

  suez: {
    resilience: 61,
    regime: "Disrupted",
    forecast: 480,
    confidence: "75%",
  },

  supplier: {
    resilience: 57,
    regime: "Supplier Risk",
    forecast: 450,
    confidence: "71%",
  },

  surge: {
    resilience: 74,
    regime: "Demand Surge",
    forecast: 720,
    confidence: "80%",
  },
  
};
const current = scenarioData[scenario];
  return (
    <div>
      <h1
        style={{
          marginBottom: "10px",
        }}
      >
        PROTEUS
      </h1>

      <p
        style={{
          color: "#9CA3AF",
          marginBottom: "40px",
        }}
      >
        Adaptive Supply Chain Intelligence Platform
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
        }}
      >
        <MetricCard title="Resilience Score" value={current.resilience} />
        <MetricCard title="Demand Regime" value={current.regime} />
        <MetricCard title="Forecast" value={current.forecast} />
        <MetricCard title="Confidence" value={current.confidence} />
      </div>

      <ForecastChart />
      <div
  style={{
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px",
    marginTop: "20px",
  }}
>
  <ModelContribution />
  <SupplyChainHealth />
  <div
  style={{
    background: "#111827",
    padding: "24px",
    borderRadius: "16px",
    marginTop: "20px",
  }}
>
  <h2>Scenario Simulator</h2>

  <div
    style={{
      display: "flex",
      gap: "10px",
      flexWrap: "wrap",
      marginTop: "20px",
    }}
  >
    <button onClick={() => setScenario("normal")}>
      Normal
    </button>

    <button onClick={() => setScenario("covid")}>
      COVID Shock
    </button>

    <button onClick={() => setScenario("suez")}>
      Suez Canal
    </button>

    <button onClick={() => setScenario("supplier")}>
      Supplier Failure
    </button>

    <button onClick={() => setScenario("surge")}>
      Demand Surge
    </button>
  </div>
</div>
</div>
    </div>
    
  );
}




export default App;