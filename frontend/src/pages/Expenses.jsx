import React, { useEffect, useState } from 'react';
import ExpenseCard from '../components/ExpenseCard';
import FormInput from '../components/FormInput';
import { getExpenses, createExpense } from '../api';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [date, setDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        const data = await getExpenses();
        setExpenses(data);
      } catch (err) {
        setError('Failed to load expenses');
      } finally {
        setLoading(false);
      }
    };
    fetchExpenses();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newExpense = await createExpense({ description, amount, date });
      setExpenses([...expenses, newExpense]);
      setSuccess('Expense added successfully');
      setDescription('');
      setAmount('');
      setDate('');
    } catch (err) {
      setError('Failed to add expense');
    }
  };

  if (loading) return <div className="text-center mt-10">Loading...</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Expenses</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {success && <p className="text-green-500 mb-4">{success}</p>}
      <form onSubmit={handleSubmit} className="mb-8">
        <FormInput label="Description" value={description} onChange={(e) => setDescription(e.target.value)} required />
        <FormInput label="Amount" type="number" value={amount} onChange={(e) => setAmount(e.target.value)} required />
        <FormInput label="Date" type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Add Expense
        </button>
      </form>
      <div>
        {expenses.map((exp) => (
          <ExpenseCard key={exp.id} expense={exp} />
        ))}
      </div>
    </div>
  );
};

export default Expenses;