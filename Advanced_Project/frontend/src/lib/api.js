import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const getProfile = async () => {
  const res = await api.get('/profile');
  return res.data;
};

export const getMemory = async () => {
  const res = await api.get('/memory');
  return res.data;
};

export const analyzeInput = async (text) => {
  const res = await api.post('/analyze', { input_text: text });
  return res.data;
};

export const simulateScenario = async (scenario) => {
  const res = await api.post('/simulate', { scenario });
  return res.data;
};

export const chatWithTwin = async (message) => {
  const res = await api.post('/chat', { message });
  return res.data;
};

export default api;
