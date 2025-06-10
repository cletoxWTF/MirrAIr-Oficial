<template>
  <div class="benchmark">
    <h1>Benchmarking para IAs</h1>
    
    <div class="input-section">
      <div class="option-card">
        <h2>Escriba las reglas o adjunte un archivo</h2>
        <textarea v-model="rules" placeholder="Escribe tus reglas aquí..." class="rules-textarea"></textarea>
        
        <div class="buttons-row">
          <div class="file-upload">
            <input type="file" accept=".txt,.hrf" @change="handleFileUpload" class="file-input" id="fileInput">
            <label for="fileInput" class="upload-button">Adjuntar archivo (.txt o .hrf)</label>
            <span v-if="fileName" class="file-name">{{ fileName }}</span>
          </div>
          
          <button @click="submitBenchmark" class="submit-button">Enviar</button>
        </div>
      </div>
    </div>
    
    <div class="models-section">
      <div class="model-column">
        <h3>ChatGPT</h3>
        <img src="https://cdn.pixabay.com/photo/2023/05/08/00/43/chatgpt-7977357_1280.png" alt="ChatGPT Logo" class="model-logo">
        <button @click="downloadChatGPT" class="download-button">Descargar traducción</button>
      </div>
      
      <div class="model-column">
        <h3>DeepSeek</h3>
        <img src="https://brandlogos.net/wp-content/uploads/2025/02/deepseek_logo_icon-logo_brandlogos.net_s5bgc-512x389.png" alt="DeepSeek Logo" class="model-logo">
        <button @click="downloadDeepSeek" class="download-button">Descargar traducción</button>
      </div>
    </div>
    
    <div class="compare-section">
      <button @click="compareResults" class="compare-button">Comparar</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BenchmarkView',
  data() {
    return {
      rules: '',
      file: null,
      fileName: '',
      loading: false
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
      this.fileName = this.file ? this.file.name : '';
    },
    async submitBenchmark() {
      this.loading = true;
      
      try {
        // Simulamos la llamada a la API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Aquí iría la lógica real para procesar el benchmark
        alert('Benchmark enviado correctamente');
        
      } catch (error) {
        console.error('Error en el benchmark:', error);
        alert('Error al procesar el benchmark');
      } finally {
        this.loading = false;
      }
    },
    downloadChatGPT() {
      alert('Descargando traducción de ChatGPT...');
      // Lógica real para descargar el resultado de ChatGPT
    },
    downloadDeepSeek() {
      alert('Descargando traducción de DeepSeek...');
      // Lógica real para descargar el resultado de DeepSeek
    },
    compareResults() {
    // Lógica para comparar resultados
    this.$router.push('/metrics');
    }
  }
};
</script>

<style scoped>
.benchmark {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

.input-section {
  margin-bottom: 40px;
}

.option-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.option-card h2 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.rules-textarea {
  width: 100%;
  height: 200px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical;
  font-family: monospace;
  margin-bottom: 20px;
}

.buttons-row {
  display: flex;
  gap: 15px;
  align-items: center;
}

.file-upload {
  position: relative;
  display: inline-block;
}

.file-input {
  display: none;
}

.upload-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.9rem;
}

.upload-button:hover {
  background-color: #2980b9;
}

.file-name {
  margin-left: 10px;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.submit-button {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #27ae60;
}

.models-section {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.model-column {
  flex: 1;
  text-align: center;
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.model-column h3 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.model-logo {
  max-width: 120px;
  max-height: 120px;
  margin: 15px auto;
  display: block;
}

.download-button {
  background-color: #9b59b6;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s;
}

.download-button:hover {
  background-color: #8e44ad;
}

.compare-section {
  text-align: center;
}

.compare-button {
  background-color: #e67e22;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.compare-button:hover {
  background-color: #d35400;
}

@media (max-width: 768px) {
  .models-section {
    flex-direction: column;
  }
  
  .buttons-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>