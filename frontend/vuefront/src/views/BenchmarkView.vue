<template>
  <div class="benchmark-container">
    <h1 class="title">Benchmarking de Modelos de Lenguaje</h1>

    <!-- Mensajes de error -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
      <button @click="errorMessage = ''" class="close-button">×</button>
    </div>

    <!-- Sección de entrada -->
    <div class="input-section">
      <div class="card">
        <h2>Ingrese su texto o suba un archivo</h2>
        <div class="input-methods">
          <!-- Método 1: Textarea -->
          <div class="method" :class="{ 'active': inputMethod === 'text' }">
            <h3>Escribir texto</h3>
            <textarea
              v-model="textInput"
              placeholder="Escribe aquí el texto a analizar..."
              class="text-input"
              @focus="inputMethod = 'text'"
            ></textarea>
          </div>
          
          <!-- Método 2: Subir archivo -->
          <div class="method" :class="{ 'active': inputMethod === 'file' }">
            <h3>Subir archivo</h3>
            <div class="file-upload-area" @click="triggerFileInput">
              <div v-if="!selectedFile" class="upload-prompt">
                <i class="fas fa-cloud-upload-alt"></i>
                <p>Arrastra un archivo aquí o haz clic para seleccionar</p>
                <p class="formats">Formatos aceptados: .txt, .hrf</p>
              </div>
              <div v-else class="file-info">
                <i class="fas fa-file-alt"></i>
                <p>{{ selectedFile.name }}</p>
                <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
              <input
                type="file"
                ref="fileInput"
                @change="handleFileSelect"
                accept=".txt,.hrf"
                style="display: none;"
              >
            </div>
          </div>
        </div>

        <button
          @click="runBenchmark"
          class="submit-button"
          :disabled="!isFormValid || processing"
        >
          <span v-if="!processing">Ejecutar Benchmark</span>
          <span v-else class="loading">
            <i class="fas fa-spinner fa-spin"></i> Procesando...
          </span>
        </button>
      </div>
    </div>

    <!-- Resultados -->
    <div v-if="results" class="results-section">
      <div class="models-comparison">
        <!-- Resultado ChatGPT -->
        <div class="model-result">
          <div class="model-header">
            <img src="https://cdn.pixabay.com/photo/2023/05/08/00/43/chatgpt-7977357_1280.png" alt="ChatGPT">
            <h3>ChatGPT</h3>
          </div>
          <div class="result-content">
            <div class="result-text" v-html="formatResponse(results.chatgpt)"></div>
            <button @click="downloadResult('chatgpt')" class="download-btn">
              <i class="fas fa-download"></i> Descargar
            </button>
          </div>
        </div>

        <!-- Resultado DeepSeek -->
        <div class="model-result">
          <div class="model-header">
            <img src="https://brandlogos.net/wp-content/uploads/2025/02/deepseek_logo_icon-logo_brandlogos.net_s5bgc-512x389.png" alt="DeepSeek">
            <h3>DeepSeek</h3>
          </div>
          <div class="result-content">
            <div class="result-text" v-html="formatResponse(results.deepseek)"></div>
            <button @click="downloadResult('deepseek')" class="download-btn">
              <i class="fas fa-download"></i> Descargar
            </button>
          </div>
        </div>
      </div>

      <div class="actions">
        <button @click="viewMetrics" class="metrics-button">
          <i class="fas fa-chart-bar"></i> Ver Métricas Detalladas
        </button>
        <button @click="resetForm" class="reset-button">
          <i class="fas fa-redo"></i> Nueva Prueba
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';  // ⬅️ ESTA LÍNEA ES CLAVE

export default {
  name: 'BenchmarkView',
  data() {
    return {
      inputMethod: 'text', // 'text' o 'file'
      textInput: '',
      selectedFile: null,
      processing: false,
      errorMessage: '',
      results: null,
      apiBaseUrl: 'http://localhost:8000/api', // Ajusta según tu configuración
    };
  },
  computed: {
    isFormValid() {
      return this.textInput.trim() !== '' || this.selectedFile !== null;
    }
  },
  methods: {
    triggerFileInput() {
      this.inputMethod = 'file';
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        // Validar tipo de archivo
        const validTypes = ['.txt', '.hrf'];
        const fileExt = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!validTypes.includes(fileExt)) {
          this.errorMessage = 'Solo se aceptan archivos .txt o .hrf';
          return;
        }

        // Validar tamaño (ejemplo: 5MB máximo)
        if (file.size > 5 * 1024 * 1024) {
          this.errorMessage = 'El archivo es demasiado grande (máximo 5MB)';
          return;
        }

        this.selectedFile = file;
        this.textInput = ''; // Limpiar textarea si había texto
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    async runBenchmark() {
      this.processing = true;
      this.errorMessage = '';
      this.results = null;

      try {
        const response = await api.sendBenchmark({
          text: this.selectedFile ? '' : this.textInput,
          file: this.selectedFile
        });

        if (response) {
          this.results = {
            id: response.id,
            chatgpt: response.chatgpt,
            deepseek: response.deepseek,
            metrics: response.metrics
          };
        }
      } catch (error) {
        this.handleApiError(error);
      } finally {
        this.processing = false;
      }
    },
    async readFile(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
      });
    },
    handleApiError(error) {
      if (error.response) {
        // Error de la API
        if (error.response.status === 400) {
          this.errorMessage = error.response.data.error || 'Datos inválidos enviados al servidor';
        } else if (error.response.status === 413) {
          this.errorMessage = 'El archivo es demasiado grande para procesar';
        } else if (error.response.status === 415) {
          this.errorMessage = 'Tipo de archivo no soportado';
        } else if (error.response.status === 500) {
          this.errorMessage = 'Error interno del servidor. Por favor, inténtalo de nuevo más tarde.';
        } else {
          this.errorMessage = `Error del servidor: ${error.response.status}`;
        }
      } else if (error.request) {
        // La petición fue hecha pero no hubo respuesta
        this.errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión.';
      } else {
        // Error al configurar la petición
        this.errorMessage = 'Error al preparar la solicitud';
      }
      
      console.error('Error detallado:', error);
    },
    formatResponse(text) {
      // Formatea el texto para mostrar saltos de línea correctamente
      if (!text) return '';
      return text.replace(/\n/g, '<br>');
    },
    downloadResult(model) {
      if (!this.results) return;
      
      const content = model === 'chatgpt' ? this.results.chatgpt : this.results.deepseek;
      const blob = new Blob([content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      
      link.href = url;
      link.download = `resultado_${model}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    },
    viewMetrics() {
      if (this.results && this.results.id) {
        this.$router.push({
          name: 'metrics',
          query: { result_id: this.results.id }
        });
      } else {
        console.error('No se encontró ID para la métrica.');
      }
    },
    resetForm() {
      this.textInput = '';
      this.selectedFile = null;
      this.results = null;
      this.inputMethod = 'text';
    }
  }
};
</script>

<style scoped>
/* Estilos generales */
.benchmark-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2.2rem;
}

/* Sección de entrada */
.input-section {
  margin-bottom: 3rem;
}

.card {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card h2 {
  margin-top: 0;
  color: #34495e;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.input-methods {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.method {
  flex: 1;
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.method.active {
  border-color: #3498db;
  background-color: #f8fafc;
}

.method h3 {
  margin-top: 0;
  color: #7f8c8d;
  font-size: 1.1rem;
  text-align: center;
}

.text-input {
  width: 100%;
  height: 200px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
}

.file-upload-area {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.file-upload-area:hover {
  background-color: #f0f0f0;
}

.upload-prompt {
  text-align: center;
  color: #7f8c8d;
}

.upload-prompt i {
  font-size: 2.5rem;
  color: #3498db;
  margin-bottom: 1rem;
}

.formats {
  font-size: 0.9rem;
  color: #95a5a6;
  margin-top: 0.5rem;
}

.file-info {
  text-align: center;
}

.file-info i {
  font-size: 2rem;
  color: #3498db;
  margin-bottom: 0.5rem;
}

.file-size {
  font-size: 0.9rem;
  color: #95a5a6;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #2980b9;
}

.submit-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.loading {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

/* Mensajes de error */
.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 1rem;
  border-radius: 5px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-button {
  background: none;
  border: none;
  color: #c62828;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 0.5rem;
}

/* Resultados */
.results-section {
  margin-top: 3rem;
}

.models-comparison {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.model-result {
  flex: 1;
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.model-header {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.model-header img {
  width: 40px;
  height: 40px;
  object-fit: contain;
  margin-right: 1rem;
}

.model-header h3 {
  margin: 0;
  color: #2c3e50;
}

.result-content {
  padding: 1.5rem;
}

.result-text {
  height: 300px;
  overflow-y: auto;
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #34495e;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #e3f2fd;
  color: #1976d2;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.download-btn:hover {
  background-color: #bbdefb;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.metrics-button {
  padding: 0.75rem 1.5rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.metrics-button:hover {
  background-color: #388e3c;
}

.reset-button {
  padding: 0.75rem 1.5rem;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.reset-button:hover {
  background-color: #d32f2f;
}

/* Responsive */
@media (max-width: 768px) {
  .input-methods {
    flex-direction: column;
  }
  
  .models-comparison {
    flex-direction: column;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>