<template>
  <div class="metrics-view">
    <h1>RESULTADOS</h1>
    
    <div class="metrics-container">
      <!-- Columna de Similitud -->
      <div class="metric-card">
        <h2>SIMILITUD</h2>
        <div class="progress-container">
          <circle-progress
            :percent="similarity"
            :size="200"
            :border-width="15"
            :border-bg-width="15"
            fill-color="#3498db"
            empty-color="#eee"
          />
          <div class="percentage-display">{{ similarity }}%</div>
        </div>
      </div>
      
      <!-- Columna de Complejidad -->
      <div class="metric-card">
        <h2>COMPLEJIDAD</h2>
        <div class="progress-container">
          <circle-progress
            :percent="complexity"
            :size="200"
            :border-width="15"
            :border-bg-width="15"
            fill-color="#e74c3c"
            empty-color="#eee"
          />
          <div class="percentage-display">{{ complexity }}%</div>
        </div>
      </div>
    </div>
    
    <button @click="toggleDetails" class="details-button">DETALLES</button>
    
    <div v-if="showDetails" class="details-content">
      <div class="metric-row">
        <span class="metric-label">JACCARD:</span>
        <span class="metric-value">10</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">COSENO:</span>
        <span class="metric-value">50</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">FRE:</span>
        <span class="metric-value">10</span>
      </div>
    </div>
    
    <button @click="evaluateAnother" class="evaluate-button">EVALUAR OTRO TEXTO</button>
  </div>
</template>

<script>
import CircleProgress from "vue3-progress";

export default {
  name: 'MetricsView',
  components: {
    CircleProgress
  },
  data() {
    return {
      similarity: 60, // Valor de ejemplo para similitud
      complexity: 70, // Valor de ejemplo para complejidad
      showDetails: false
    };
  },
  methods: {
    toggleDetails() {
      this.showDetails = !this.showDetails;
    },
    evaluateAnother() {
      this.$router.push('/benchmark');
    }
  }
};
</script>

<style scoped>
.metrics-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 40px;
  font-size: 2.2rem;
}

.metrics-container {
  display: flex;
  justify-content: space-around;
  gap: 30px;
  margin-bottom: 40px;
}

.metric-card {
  flex: 1;
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.metric-card h2 {
  margin-top: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.progress-container {
  position: relative;
  margin: 0 auto;
  width: 200px;
  height: 200px;
}

.percentage-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.details-button {
  background-color: #9b59b6;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 30px;
  transition: background-color 0.3s;
}

.details-button:hover {
  background-color: #8e44ad;
}

.details-content {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  max-width: 400px;
  margin: 0 auto 30px;
  text-align: left;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.metric-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  font-size: 1.1rem;
}

.metric-row:last-child {
  border-bottom: none;
}

.metric-label {
  font-weight: bold;
  color: #2c3e50;
}

.metric-value {
  color: #7f8c8d;
  font-weight: 500;
}

.evaluate-button {
  background-color: #e67e22;
  color: white;
  border: none;
  padding: 14px 40px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.evaluate-button:hover {
  background-color: #d35400;
}

@media (max-width: 768px) {
  .metrics-container {
    flex-direction: column;
  }
  
  .metric-card {
    max-width: 300px;
    margin: 0 auto;
  }
}
</style>