<template>
  <div class="home">
    <section class="hero">
      <h1>Bienvenido a MirrAIr</h1>
      <p>El mejor analista de IA</p>
      <img src="@/assets/img/pug.jpeg" alt="MirrAIr" class="hero-image">
    </section>

    <section class="verification">
      <div class="verification-container">
        <h2>Veracidad en nuestros resultados</h2>
        <div class="verification-content">
          <p>Nuestro sistema utiliza tecnología avanzada para asegurar resultados exactos mediante algunas métricas</p>
          <div class="verification-result">
            <p>Resultados comprobado por expertos</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
};
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 40px 20px;
  background-color: #f0f8ff;
}

.hero-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.verification {
  margin: 40px 0;
}

.verification-container {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.verification-content {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #eaeaea;
  border-radius: 8px;
}
</style>