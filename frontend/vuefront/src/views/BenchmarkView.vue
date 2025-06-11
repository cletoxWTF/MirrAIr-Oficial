<template>
  <div class="benchmark">
    <h1>Benchmarking para IAs</h1>

    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>

    <div class="input-section">
      <div class="option-card">
        <h2>Escriba las reglas o adjunte un archivo</h2>

        <textarea
          v-model="rules"
          placeholder="Escribe tus reglas aquí..."
          class="rules-textarea"
          :disabled="isFileAttached"
          @input="handleTextInput"
        ></textarea>

        <div class="buttons-row">
          <div class="file-upload">
            <input
              type="file"
              accept=".txt,.hrf"
              @change="handleFileUpload"
              class="file-input"
              id="fileInput"
              :disabled="isTextEntered"
            />
            <label for="fileInput" class="upload-button">Adjuntar archivo (.txt o .hrf)</label>
            <span v-if="fileName" class="file-name">{{ fileName }}</span>
          </div>

          <button
            @click="submitBenchmark"
            class="submit-button"
            :disabled="!isTextEntered && !isFileAttached"
          >
            Enviar
          </button>
        </div>
      </div>
    </div>

    <div class="models-section">
      <div class="model-column">
        <h3>ChatGPT (Simulado)</h3>
        <img
          src="https://cdn.pixabay.com/photo/2023/05/08/00/43/chatgpt-7977357_1280.png"
          alt="ChatGPT Logo"
          class="model-logo"
        />
        <div v-if="chatGPTResponse">
          <p>{{ chatGPTResponse }}</p>
          <button @click="downloadChatGPT" class="download-button">Descargar traducción</button>
        </div>
      </div>

      <div class="model-column">
        <h3>DeepSeek</h3>
        <img
          src="https://brandlogos.net/wp-content/uploads/2025/02/deepseek_logo_icon-logo_brandlogos.net_s5bgc-512x389.png"
          alt="DeepSeek Logo"
          class="model-logo"
        />
        <div v-if="deepSeekResponse">
          <p>{{ deepSeekResponse }}</p>
          <button @click="downloadDeepSeek" class="download-button">Descargar traducción</button>
        </div>
      </div>
    </div>

    <div class="compare-section">
      <button 
        @click="compareResults" 
        class="compare-button" 
        :disabled="!canCompare"
      >
        Comparar
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BenchmarkView",
  data() {
    return {
      rules: "",
      file: null,
      fileName: "",
      isTextEntered: false, // Controla si el usuario ha escrito en el textarea
      isFileAttached: false, // Controla si se ha adjuntado un archivo
      loading: false,
      chatGPTResponse: "", // Respuesta de ChatGPT (Simulada)
      deepSeekResponse: "", // Respuesta de DeepSeek
      errorMessage: "", // Mensaje de error
    };
  },
  computed: {
    // Esta propiedad computada se encarga de habilitar el botón "Comparar" solo cuando ambas respuestas estén disponibles.
    canCompare() {
      return this.chatGPTResponse && this.deepSeekResponse;
    }
  },
  methods: {
    // Función para manejar cuando se escribe en el textarea
    handleTextInput() {
      this.isTextEntered = this.rules.trim() !== "";
      this.isFileAttached = false; // Si escribe, desactivar la opción de adjuntar archivo
    },

    // Función para manejar la carga de archivo
    handleFileUpload(event) {
      this.file = event.target.files[0];
      this.fileName = this.file ? this.file.name : "";
      this.isFileAttached = !!this.file;
      this.isTextEntered = false; // Si adjunta archivo, desactivar la opción de escribir
    },

    async submitBenchmark() {
      this.loading = true;
      const prompt =
        "I need you to translate the information into structured natural language and explain it to me in a paragraph in plain text format, without literals, bullet points, or HTML. I'm 15 years old.:";

      // Obtener contenido de `rules` o el archivo
      const content =
        this.rules.trim() || (await this.readFileContent(this.file));

      // Validación para asegurarse que hay contenido
      if (!content || content.trim() === "") {
        console.log("No se ingresó texto ni se seleccionó un archivo válido");
        alert("No input provided!");
        this.loading = false;
        return;
      }

      console.log("Contenido a enviar:", content); // Verifica si el contenido es correcto

      const requestPayload = {
        prompt: `${prompt}\n\n${content}`,
      };

      // Verificamos el formato del payload antes de enviarlo
      console.log("Payload antes de enviar a la API:", JSON.stringify(requestPayload));

      try {
        // Simulamos la respuesta de ChatGPT
        this.chatGPTResponse = `This is a set of rules for a Tic-Tac-Toe game written in a logical language. It defines the game's structure and how it works...`;

        // Solicitar respuesta de DeepSeek
        const deepSeekResponse = await this.fetchDeepSeekResponse(requestPayload);
        this.deepSeekResponse = deepSeekResponse;

      } catch (error) {
        console.error("Error en la consulta a las APIs:", error);
        this.errorMessage = `Error al conectar con la API: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },

    async readFileContent(file) {
      if (file) {
        const reader = new FileReader();
        return new Promise((resolve, reject) => {
          reader.onload = () => {
            console.log("Contenido del archivo leído:", reader.result); // Verifica el contenido leído
            resolve(reader.result);
          };
          reader.onerror = reject;
          reader.readAsText(file);
        });
      }
      return "";
    },

    async fetchDeepSeekResponse(payload) {
      try {
        if (!payload || typeof payload !== "object" || !payload.prompt) {
          throw new Error("El contenido del mensaje está vacío o mal formado.");
        }

        // Verificamos que el payload tenga la estructura correcta
        console.log("Verificando estructura del payload antes de enviarlo:", payload);

        // Realizamos la llamada a la API para obtener la respuesta de DeepSeek
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
          method: "POST",
          headers: {
            Authorization:
              "Bearer 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",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8080/", // Opcional
            "X-Title": "MirrAIr", // Opcional
          },
          body: JSON.stringify({
            model: "deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages: [
              {
                role: "user",
                content: payload.prompt,
              },
            ],
          }),
        });

        // Verificamos si la respuesta es exitosa
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Error en la solicitud: ${response.status} ${response.statusText}. Detalles: ${errorText}`
          );
        }

        // Obtener el texto de la respuesta
        let data;
        const contentType = response.headers.get("Content-Type");
        if (contentType && contentType.includes("application/json")) {
          data = await response.json(); // Convertir la respuesta a JSON
        } else {
          const text = await response.text();
          throw new Error(`Respuesta no es JSON, recibió: ${text}`);
        }

        if (data?.choices?.[0]?.message?.content) {
          return data.choices[0].message.content;
        } else {
          throw new Error("Respuesta de DeepSeek inválida o vacía.");
        }
      } catch (error) {
        console.error("Error al obtener la respuesta de DeepSeek:", error);
        this.errorMessage = `Error al conectar con DeepSeek: ${error.message}`;
        throw error;
      }
    },

    // Funciones de descarga
    downloadChatGPT() {
      const blob = new Blob([this.chatGPTResponse], { type: "text/plain" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "chatgpt_translation.txt";
      link.click();
    },

    downloadDeepSeek() {
      const blob = new Blob([this.deepSeekResponse], { type: "text/plain" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "deepseek_translation.txt";
      link.click();
    },

    compareResults() {
      this.$router.push({ name: "metrics" });
    },
  },
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

.responses-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.error-message {
  color: red;
  background-color: #ffcccc;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
}
</style>
