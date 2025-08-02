import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

interface BurnoutChartProps {
  history: number[];
}

const BurnoutChart: React.FC<BurnoutChartProps> = ({ history }) => {
  const data = history.map((score, index) => ({
    day: `Day ${index + 1}`,
    score,
  }));

  return (
    <div style={{ width: "100%", height: 300, marginTop: "2rem" }}>
      <h2 className="text-lg font-semibold mb-2">Burnout Trend (Last 7 Days)</h2>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Line type="monotone" dataKey="score" stroke="#ef4444" strokeWidth={2} dot />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BurnoutChart;