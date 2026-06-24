import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

const data = [
  { day: "Mon", demand: 450 },
  { day: "Tue", demand: 480 },
  { day: "Wed", demand: 510 },
  { day: "Thu", demand: 530 },
  { day: "Fri", demand: 550 },
  { day: "Sat", demand: 580 },
  { day: "Sun", demand: 610 },
];

function ForecastChart() {
  return (
    <div
      style={{
        background: "#111827",
        marginTop: "30px",
        padding: "24px",
        borderRadius: "16px",
        height: "400px",
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>
        Demand Forecast
      </h2>

      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="day" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="demand"
            stroke="#22C55E"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ForecastChart;