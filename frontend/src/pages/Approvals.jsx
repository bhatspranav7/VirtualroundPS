import React, { useEffect, useState } from 'react';
import ApprovalCard from '../components/ApprovalCard';
import { getApprovals, approveApproval, rejectApproval } from '../api';

const Approvals = () => {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchApprovals = async () => {
      try {
        const data = await getApprovals();
        setApprovals(data);
      } catch (err) {
        setError('Failed to load approvals');
      } finally {
        setLoading(false);
      }
    };
    fetchApprovals();
  }, []);

  const handleApprove = async (id) => {
    try {
      await approveApproval(id);
      setApprovals(approvals.filter((app) => app.id !== id));
    } catch (err) {
      setError('Failed to approve');
    }
  };

  const handleReject = async (id) => {
    try {
      await rejectApproval(id);
      setApprovals(approvals.filter((app) => app.id !== id));
    } catch (err) {
      setError('Failed to reject');
    }
  };

  if (loading) return <div className="text-center mt-10">Loading...</div>;
  if (error) return <div className="text-red-500 text-center mt-10">{error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Approvals</h1>
      <div>
        {approvals.map((app) => (
          <ApprovalCard key={app.id} approval={app} onApprove={handleApprove} onReject={handleReject} />
        ))}
      </div>
    </div>
  );
};

export default Approvals;