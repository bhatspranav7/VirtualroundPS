import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (credentials) => {
  const { data } = await api.post('/auth/login', credentials);
  return data;
};

export const getExpenses = async () => {
  const { data } = await api.get('/expenses');
  return data;
};

export const createExpense = async (expense) => {
  const { data } = await api.post('/expenses', expense);
  return data;
};

export const getApprovals = async () => {
  const { data } = await api.get('/approvals');
  return data;
};

export const approveApproval = async (id) => {
  const { data } = await api.put(`/approvals/${id}/approve`);
  return data;
};

export const rejectApproval = async (id) => {
  const { data } = await api.put(`/approvals/${id}/reject`);
  return data;
};

export const getUsers = async () => {
  const { data } = await api.get('/users');
  return data;
};