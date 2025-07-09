<template>
  <div class="metrics-container">
    <h1 class="title">RESULTADOS</h1>

    <div class="metrics">
      <!-- SIMILITUD -->
      <div class="metric">
        <div class="progress-circle">
          <svg width="100" height="100">
            <circle cx="50" cy="50" r="45" stroke="#e6e6e6" stroke-width="10" fill="none" />
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="#007bff"
              stroke-width="10"
              fill="none"
              :stroke-dasharray="2 * Math.PI * 45"
              :stroke-dashoffset="2 * Math.PI * 45 * (1 - similarity / 100)"
              stroke-linecap="round"
              transform="rotate(-90 50 50)"
            />
          </svg>
        </div>
        <h2>SIMILITUD</h2>
        <p class="percentage">{{ similarity.toFixed(2) }}%</p>
      </div>

      <!-- COMPLEJIDAD CHATGPT -->
      <div class="metric">
        <div class="progress-circle">
          <svg width="100" height="100">
            <circle cx="50" cy="50" r="45" stroke="#e6e6e6" stroke-width="10" fill="none" />
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="#28a745"
              stroke-width="10"
              fill="none"
              :stroke-dasharray="2 * Math.PI * 45"
              :stroke-dashoffset="2 * Math.PI * 45 * (1 - complexity_chatgpt / 100)"
              stroke-linecap="round"
              transform="rotate(-90 50 50)"
            />
          </svg>
        </div>
        <h2>COMPLEJIDAD CHATGPT</h2>
        <p class="percentage">{{ complexity_chatgpt.toFixed(2) }}%</p>
      </div>

      <!-- COMPLEJIDAD DEEPSEEK -->
      <div class="metric">
        <div class="progress-circle">
          <svg width="100" height="100">
            <circle cx="50" cy="50" r="45" stroke="#e6e6e6" stroke-width="10" fill="none" />
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="#ff5733"
              stroke-width="10"
              fill="none"
              :stroke-dasharray="2 * Math.PI * 45"
              :stroke-dashoffset="2 * Math.PI * 45 * (1 - complexity_deepseek / 100)"
              stroke-linecap="round"
              transform="rotate(-90 50 50)"
            />
          </svg>
        </div>
        <h2>COMPLEJIDAD DEEPSEEK</h2>
        <p class="percentage">{{ complexity_deepseek.toFixed(2) }}%</p>
      </div>
    </div>

    <div class="buttons">
      <button @click="toggleDetails" class="details">DETALLES</button>
      <button @click="evaluateAnother" class="evaluate">EVALUAR OTRO TEXTO</button>
    </div>

    <div v-if="showDetails" class="details-list">
      <h3>Detalles de Métricas:</h3>
      <ul>
        <li>Similitud de Jaccard: {{ metrics.jaccard.toFixed(2) }}</li>
        <li>Similitud de Coseno: {{ metrics.cosine.toFixed(2) }}</li>
        <li>Distancia de Levenshtein: {{ metrics.levenshtein }}</li>
      </ul>
      <h4>ChatGPT:</h4>
      <ul>
        <li>FRE: {{ metrics.chatgpt.fre.toFixed(2) }}</li>
        <li>SMOG Index: {{ metrics.chatgpt.smog.toFixed(2) }}</li>
        <li>UniEval: {{ metrics.chatgpt.unieval.toFixed(2) }}</li>
      </ul>
      <h4>DeepSeek:</h4>
      <ul>
        <li>FRE: {{ metrics.deepseek.fre.toFixed(2) }}</li>
        <li>SMOG Index: {{ metrics.deepseek.smog.toFixed(2) }}</li>
        <li>UniEval: {{ metrics.deepseek.unieval.toFixed(2) }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MetricsView',
  data() {
    return {
      similarity: 0,
      complexity_chatgpt: 0,
      complexity_deepseek: 0,
      showDetails: false,
      metrics: {
        jaccard: 0,
        cosine: 0,
        levenshtein: 0,
        chatgpt: {
          fre: 0,
          smog: 0,
          unieval: 0
        },
        deepseek: {
          fre: 0,
          smog: 0,
          unieval: 0
        }
      }
    };
  },
  async mounted() {
    const resultId = this.$route.query.result_id;
    console.log('Result ID from query:', resultId);
    if (resultId) {
      try {
        const response = await axios.get(`http://localhost:8000/api/metrics/${resultId}/`);
        console.log('API response:', response.data);

        this.similarity = response.data.similarity || 0;
        this.complexity_chatgpt = response.data.complexity_chatgpt || 0;
        this.complexity_deepseek = response.data.complexity_deepseek || 0;

        this.metrics = {
          jaccard: response.data.similarity_details.jaccard,
          cosine: response.data.similarity_details.cosine,
          levenshtein: response.data.similarity_details.levenshtein,
          chatgpt: response.data.details_chatgpt,
          deepseek: response.data.details_deepseek
        };

      } catch (error) {
        console.error('Error loading metrics:', error);
      }
    }
  },

  methods: {
    toggleDetails() {
      this.showDetails = !this.showDetails;
    },
    evaluateAnother() {
      this.$router.push({ name: 'benchmark' });
    }
  }
};
</script>

<style scoped>
.metrics-container {
  text-align: center;
  padding: 2rem;
  background: #f5f5f5;
  min-height: 100vh;
}
.title {
  font-size: 2rem;
  margin-bottom: 2rem;
}
.metrics {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.metric {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 200px;
}
.percentage {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}
.buttons {
  margin-top: 1rem;
}
.details {
  background-color: #9b59b6;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  margin-right: 1rem;
  cursor: pointer;
}
.evaluate {
  background-color: #e67e22;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.details-list {
  margin-top: 2rem;
  text-align: left;
  display: inline-block;
  background: #fff;
  padding: 1rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
