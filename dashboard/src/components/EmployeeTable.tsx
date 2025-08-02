import React from "react";
import { Link } from "react-router-dom";
import { Employee } from "../types/Employee";

interface Props {
  data: Employee[];
}

const getStatus = (daysToBurnout: number): "Healthy" | "Warning" | "Critical" => {
  if (daysToBurnout <= 5) return "Critical";
  if (daysToBurnout <= 14) return "Warning";
  return "Healthy";
};

const getStatusColor = (status: string): string => {
  switch (status) {
    case "Critical":
      return "#dc2626";
    case "Warning":
      return "#f59e0b";
    default:
      return "#16a34a";
  }
};

const EmployeeTable: React.FC<Props> = ({ data }) => {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
      <thead>
        <tr>
          <th>Name</th>
          <th>Department</th>
          <th>Role</th>
          <th>Productivity</th>
          <th>Burnout Score</th>
          <th>Burnout in (days)</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {data.map((emp) => {
          const status = getStatus(emp.daysToBurnout);
          const statusColor = getStatusColor(status);

          return (
            <tr key={emp.id}>
              <td colSpan={7}>
                <Link
                  to={`/employee/${emp.id}`}
                  style={{
                    display: "block",
                    padding: "8px",
                    textDecoration: "none",
                    color: "inherit",
                    border: "1px solid #e5e7eb",
                    borderRadius: "4px",
                    marginBottom: "8px",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span>{emp.name}</span>
                    <span>{emp.department}</span>
                    <span>{emp.role}</span>
                    <span>{emp.productivityScore}</span>
                    <span>{emp.burnoutScore}</span>
                    <span>{emp.daysToBurnout}</span>
                    <span style={{ color: statusColor, fontWeight: "bold" }}>
                      {status}
                    </span>
                  </div>
                </Link>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default EmployeeTable;