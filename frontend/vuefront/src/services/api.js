import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Accept': 'application/json'
  }
});

export default {
  /**
   * Envía texto o archivo para procesar benchmark
   * @param {Object} options
   * @param {string} [options.text]
   * @param {File} [options.file]
   */
  async sendBenchmark({ text = '', file = null }) {
    try {
      let payload;
      let headers;

      if (file) {
        payload = new FormData();
        payload.append('file', file);
        headers = { 'Content-Type': 'multipart/form-data' };
      } else {
        payload = { text };
        headers = { 'Content-Type': 'application/json' };
      }

      const response = await api.post('/benchmark/', payload, { headers });
      return response.data;
    } catch (error) {
      console.error('API Error:', error.response || error);
      throw error;
    }
  },

  async getMetrics(resultId) {
    try {
      const response = await api.get(`/metrics/${resultId}/`);
      return response.data;
    } catch (error) {
      console.error('API Error:', error.response || error);
      throw error;
    }
  }
};
