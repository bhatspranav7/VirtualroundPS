import React from 'react';

const ExpenseCard = ({ expense }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4">
      <h3 className="text-lg font-bold">{expense.description}</h3>
      <p className="text-gray-600">Amount: ${expense.amount}</p>
      <p className="text-gray-600">Date: {expense.date}</p>
      <p className="text-gray-600">Status: {expense.status}</p>
    </div>
  );
};

export default ExpenseCard;