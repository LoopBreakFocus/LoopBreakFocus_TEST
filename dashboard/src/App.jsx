import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import EmployeeDetails from './pages/EmployeeDetails';
import Tst from './pages/tst';

const App = () => {
  return (
    <BrowserRouter basename="/hr">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/employee/:id" element={<EmployeeDetails />} />
        <Route path="/test" element={<Tst />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;