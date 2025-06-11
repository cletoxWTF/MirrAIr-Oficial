<template>
  <div class="metrics-container">
    <h1 class="title">RESULTADOS</h1>

    <div class="metrics">
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
        <p class="percentage">{{ similarity }}%</p>
      </div>

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
              :stroke-dashoffset="2 * Math.PI * 45 * (1 - complexity / 100)"
              stroke-linecap="round"
              transform="rotate(-90 50 50)"
            />
          </svg>
        </div>
        <h2>COMPLEJIDAD</h2>
        <p class="percentage">{{ complexity }}%</p>
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
        <li>FRE (Flesch Reading Ease): {{ metrics.fre.toFixed(2) }}</li>
        <li>SMOG Index: {{ metrics.smog.toFixed(2) }}</li>
        <li>UniEval: {{ metrics.unieval.toFixed(2) }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { distance as levenshtein } from 'fastest-levenshtein';

export default {
  name: 'MetricsView',
  data() {
    return {
      similarity: 0,
      complexity: 0,
      showDetails: false,
      metrics: {
        jaccard: 0,
        cosine: 0,
        fre: 0,
        smog: 0,
        levenshtein: 0,
        unieval: 0
      }
    };
  },
  computed: {
    chatgptText() {
      return this.$route.params.chatgpt || '';
    },
    deepseekText() {
      return this.$route.params.deepseek || '';
    }
  },
  mounted() {
    this.calculateMetrics();
  },
  methods: {
    toggleDetails() {
      this.showDetails = !this.showDetails;
    },
    evaluateAnother() {
      this.$router.push({ name: 'benchmark' });
    },
    calculateMetrics() {
      const text1 = this.chatgptText;
      const text2 = this.deepseekText;

      const jaccard = this.jaccardSimilarity(text1, text2);
      const cosine = this.cosineSimilarity(text1, text2);
      const lev = levenshtein(text1, text2);
      const fre = this.fleschReadingEase(text2);
      const smog = this.smogIndex(text2);
      const unieval = this.simulateUniEval(text2);

      const similarityPercent = ((jaccard + cosine + (1 - lev / Math.max(text1.length, 1))) / 3) * 100;
      const complexityPercent = (this.normalizeFRE(fre) + this.normalizeSMOG(smog) + unieval) / 3;

      this.metrics = { jaccard, cosine, fre, smog, levenshtein: lev, unieval };
      this.similarity = Math.round(similarityPercent);
      this.complexity = Math.round(complexityPercent);
    },
    simulateUniEval(text) {
      const length = text.length;
      if (length < 100) return 40;
      if (length < 250) return 60;
      if (length < 500) return 75;
      return 90;
    },
    jaccardSimilarity(str1, str2) {
      const a = new Set(str1.toLowerCase().split(/\s+/));
      const b = new Set(str2.toLowerCase().split(/\s+/));
      const inter = new Set([...a].filter(x => b.has(x)));
      const union = new Set([...a, ...b]);
      return inter.size / union.size || 0;
    },
    cosineSimilarity(str1, str2) {
      const getFrequency = (text) => {
        const words = text.toLowerCase().match(/\w+/g) || [];
        const freq = {};
        words.forEach(word => (freq[word] = (freq[word] || 0) + 1));
        return freq;
      };

      const freq1 = getFrequency(str1);
      const freq2 = getFrequency(str2);

      const allWords = new Set([...Object.keys(freq1), ...Object.keys(freq2)]);
      const vec1 = [], vec2 = [];

      allWords.forEach(word => {
        vec1.push(freq1[word] || 0);
        vec2.push(freq2[word] || 0);
      });

      const dot = vec1.reduce((acc, val, i) => acc + val * vec2[i], 0);
      const magnitude = (vec) => Math.sqrt(vec.reduce((acc, val) => acc + val * val, 0));
      return dot / (magnitude(vec1) * magnitude(vec2) || 1);
    },
    fleschReadingEase(text) {
      const sentences = text.split(/[.!?]/).filter(s => s.trim().length > 0).length;
      const words = text.split(/\s+/).filter(w => w.trim().length > 0).length;
      const syllables = this.countTotalSyllables(text);

      if (sentences === 0 || words === 0) return 0;

      return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words);
    },
    smogIndex(text) {
      const sentences = text.split(/[.!?]/).filter(s => s.trim().length > 0).length;
      const polysyllables = this.countPolysyllables(text);

      if (sentences === 0) return 0;

      return 1.043 * Math.sqrt(polysyllables * (30 / sentences)) + 3.1291;
    },
    countSyllables(word) {
      word = word.toLowerCase();
      if (word.length <= 3) return 1;
      word = word.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, '');
      word = word.replace(/^y/, '');
      const matches = word.match(/[aeiouy]{1,2}/g);
      return matches ? matches.length : 1;
    },
    countTotalSyllables(text) {
      const words = text.split(/\s+/).filter(w => w.trim().length > 0);
      return words.reduce((acc, word) => acc + this.countSyllables(word), 0);
    },
    countPolysyllables(text) {
      const words = text.split(/\s+/).filter(w => w.trim().length > 0);
      return words.filter(w => this.countSyllables(w) >= 3).length;
    },
    normalizeFRE(score) {
      return Math.min(Math.max(score, 0), 100);
    },
    normalizeSMOG(score) {
      const max = 18, min = 3;
      return 100 - ((score - min) / (max - min)) * 100;
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
