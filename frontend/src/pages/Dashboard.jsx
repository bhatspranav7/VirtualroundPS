import React, { useEffect, useState } from 'react';
import { getExpenses, getApprovals } from '../api';

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const exp = await getExpenses();
        const app = await getApprovals();
        setExpenses(exp);
        setApprovals(app);
      } catch (err) {
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="text-center mt-10">Loading...</div>;
  if (error) return <div className="text-red-500 text-center mt-10">{error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl">Expenses Summary</h2>
          <p>Total Expenses: {expenses.length}</p>
        </div>
        <div>
          <h2 className="text-xl">Pending Approvals</h2>
          <p>Total Pending: {approvals.length}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;