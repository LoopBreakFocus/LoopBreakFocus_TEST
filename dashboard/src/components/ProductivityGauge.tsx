// src/components/ProductivityGauge.tsx
import React from "react";
import {
  CircularProgressbar,
  buildStyles,
} from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

interface Props {
  score: number;
}

const ProductivityGauge: React.FC<Props> = ({ score }) => {
  const color =
    score < 50 ? "#dc2626" : score < 80 ? "#f59e0b" : "#16a34a"; // red, yellow, green

  return (
    <div style={{ width: 120, height: 120 }}>
      <CircularProgressbar
        value={score}
        text={`${score}%`}
        styles={buildStyles({
          pathColor: color,
          textColor: "#000",
          trailColor: "#e5e7eb",
          textSize: "16px",
        })}
      />
      <p className="text-center text-sm mt-2 font-medium">Productivity</p>
    </div>
  );
};

export default ProductivityGauge;