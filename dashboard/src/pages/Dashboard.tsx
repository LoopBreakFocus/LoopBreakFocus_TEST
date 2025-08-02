import React, { useState } from "react";
import EmployeeTable from "../components/EmployeeTable";
import employeesData from "../data/employees.json";
import { Employee } from "../types/Employee";

const Dashboard: React.FC = () => {
  const [department, setDepartment] = useState("All");
  const [status, setStatus] = useState("All");
  const [search, setSearch] = useState("");

  const employees: Employee[] = employeesData;

  const filterStatus = (days: number): string => {
    if (days <= 5) return "Critical";
    if (days <= 14) return "Warning";
    return "Healthy";
  };

  const filteredEmployees = employees.filter((emp) => {
    const matchesDepartment =
      department === "All" || emp.department === department;
    const matchesStatus =
      status === "All" || filterStatus(emp.daysToBurnout) === status;
    const matchesSearch =
      emp.name.toLowerCase().includes(search.toLowerCase());
    return matchesDepartment && matchesStatus && matchesSearch;
  });

  const uniqueDepartments = Array.from(
    new Set(employees.map((e) => e.department))
  );

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8 gap-4">
        <h1 className="text-4xl font-semibold text-gray-900">LoopBreak Dashboard</h1>
        <p className="text-sm text-gray-500">Monitor burnout patterns and team performance</p>
      </div>

      {/* Filters */}
      <div className="bg-white border border-gray-200 p-4 rounded-lg shadow-sm mb-6 flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          placeholder="Search employee"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 w-full sm:w-1/3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <select
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 w-full sm:w-1/4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="All">All Departments</option>
          {uniqueDepartments.map((dep) => (
            <option key={dep} value={dep}>{dep}</option>
          ))}
        </select>

        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 w-full sm:w-1/4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="All">All Statuses</option>
          <option value="Healthy">Healthy</option>
          <option value="Warning">Warning</option>
          <option value="Critical">Critical</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-white shadow-md rounded-xl overflow-hidden border border-gray-100">
        <EmployeeTable data={filteredEmployees} />
      </div>
    </div>
  );
};

export default Dashboard;