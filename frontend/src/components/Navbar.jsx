import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ onLogout }) => {
  return (
    <nav className="bg-blue-600 p-4 text-white flex justify-between">
      <div className="text-xl font-bold">Expense Approval System</div>
      <div className="space-x-4">
        <Link to="/dashboard" className="hover:underline">Dashboard</Link>
        <Link to="/expenses" className="hover:underline">Expenses</Link>
        <Link to="/approvals" className="hover:underline">Approvals</Link>
        <Link to="/users" className="hover:underline">Users</Link>
        <button onClick={onLogout} className="hover:underline">Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;