// src/pages/EmployeeDetails.tsx
import React, { useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import employeeData from "../data/employees.json";
import BurnoutChart from "../components/BurnoutChart";
import GoalProgress from "../components/GoalProgress";
import ProductivityGauge from "../components/ProductivityGauge";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { Info } from "lucide-react";
import * as Tooltip from "@radix-ui/react-tooltip";

interface Employee {
  id: string;
  name: string;
  department: string;
  productivityScore: number;
  burnoutScore: number;
  burnoutHistory: number[];
  lastActive: string;
  goalsCompleted: number;
  goalsTotal: number;
  suggestions: string[];
  status: string;
  role: string;
  daysToBurnout: number;
}

export default function EmployeeDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const reportRef = useRef<HTMLDivElement>(null);

  const employee: Employee | undefined = employeeData.find(emp => emp.id === id);

  const handleDownloadPDF = async () => {
    if (!reportRef.current) return;
    const canvas = await html2canvas(reportRef.current);
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save(`${employee?.name.replace(/\s+/g, "_")}_Report.pdf`);
  };

  if (!employee) {
    return (
      <div className="p-6">
        <h2 className="text-xl text-red-600">Employee not found.</h2>
        <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded" onClick={() => navigate("/")}>
          Go Back
        </button>
      </div>
    );
  }

  const burnoutColor =
    employee.daysToBurnout <= 5
      ? "bg-yellow-100 text-yellow-800"
      : employee.daysToBurnout <= 14
      ? "bg-orange-100 text-orange-800"
      : "bg-green-100 text-green-800";

  return (
    <Tooltip.Provider>
      <div className="p-6 max-w-6xl mx-auto bg-white min-h-screen">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <button
            className="px-4 py-1 border text-sm rounded hover:bg-gray-100"
            onClick={() => navigate("/")}
          >
            ← Back to Dashboard
          </button>
          <button
            className="px-4 py-1 border text-sm rounded hover:bg-gray-100"
            onClick={handleDownloadPDF}
          >
            Download PDF
          </button>
        </div>

        <div ref={reportRef} className="space-y-6">
          {/* Header */}
          <h1 className="text-4xl font-bold">{employee.name}</h1>

          {/* Info Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Left Info */}
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Department:</span> {employee.department}</p>
              <p><span className="font-medium">Role:</span> {employee.role}</p>
              <p><span className="font-medium">Status:</span> {employee.status}</p>

              {/* Estimated Burnout */}
              <div className="flex items-center gap-2">
                <span className="font-medium">Estimated Burnout:</span>
                <span className={`rounded-full px-3 py-1 text-xs font-semibold ${burnoutColor}`}>
                  {employee.daysToBurnout} days
                </span>

                <Tooltip.Root>
                  <Tooltip.Trigger asChild>
                    <button className="hover:bg-gray-100 rounded p-1">
                      <Info size={16} className="text-gray-600" />
                    </button>
                  </Tooltip.Trigger>
                  <Tooltip.Portal>
                    <Tooltip.Content className="bg-black text-white px-3 py-1 rounded text-xs z-50">
                      Based on historical burnout patterns, recent activity, and productivity scores.
                      <Tooltip.Arrow className="fill-black" />
                    </Tooltip.Content>
                  </Tooltip.Portal>
                </Tooltip.Root>
              </div>

              <p>
                <span className="font-medium">Last Active:</span>{" "}
                {new Date(employee.lastActive).toLocaleString()}
              </p>
            </div>

            {/* Productivity Circle */}
            <div className="flex flex-col items-center justify-center">
              <p className="text-sm text-gray-500 mb-1">Productivity</p>
              <ProductivityGauge score={employee.productivityScore} />
            </div>
          </div>

          <hr className="my-4" />

          {/* Goal Progress */}
          <div>
            <h2 className="text-lg font-semibold mb-2">Goal Progress</h2>
            <GoalProgress completed={employee.goalsCompleted} total={employee.goalsTotal} />
          </div>

          {/* Burnout Chart */}
          <div>
            <h2 className="text-lg font-semibold mb-2">Burnout Trend (Last 7 Days)</h2>
            <BurnoutChart history={employee.burnoutHistory.slice(-7)} />
          </div>

          {/* Suggestions */}
          <div>
            <h2 className="text-lg font-semibold mb-2">Suggestions</h2>
            <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
              {employee.suggestions.map((suggestion, i) => (
                <li key={i}>{suggestion}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </Tooltip.Provider>
  );
}