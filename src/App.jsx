import MetricCard from "./components/MetricCard";
import ForecastChart from "./components/ForecastChart";

function App() {
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
        <MetricCard title="Resilience Score" value="88" />
        <MetricCard title="Demand Regime" value="Seasonal" />
        <MetricCard title="Forecast" value="520" />
        <MetricCard title="Confidence" value="91%" />
      </div>

      <ForecastChart />
    </div>
  );
}

export default App;