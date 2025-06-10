import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  get(endpoint) {
    return api.get(endpoint);
  },
  post(endpoint, data) {
    return api.post(endpoint, data);
  },
};