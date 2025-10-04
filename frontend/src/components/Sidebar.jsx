import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="bg-gray-200 w-64 h-screen p-4">
      <ul className="space-y-4">
        <li><Link to="/dashboard" className="hover:text-blue-600">Dashboard</Link></li>
        <li><Link to="/expenses" className="hover:text-blue-600">Expenses</Link></li>
        <li><Link to="/approvals" className="hover:text-blue-600">Approvals</Link></li>
        <li><Link to="/users" className="hover:text-blue-600">Users</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;