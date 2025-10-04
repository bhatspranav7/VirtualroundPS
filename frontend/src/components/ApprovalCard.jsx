import React from 'react';

const ApprovalCard = ({ approval, onApprove, onReject }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4">
      <h3 className="text-lg font-bold">{approval.description}</h3>
      <p className="text-gray-600">Amount: ${approval.amount}</p>
      <p className="text-gray-600">Submitted by: {approval.user}</p>
      <div className="mt-4">
        <button
          onClick={() => onApprove(approval.id)}
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-2"
        >
          Approve
        </button>
        <button
          onClick={() => onReject(approval.id)}
          className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        >
          Reject
        </button>
      </div>
    </div>
  );
};

export default ApprovalCard;