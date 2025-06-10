<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="logo">MirrAIr</router-link>
      <div class="nav-links">
        <router-link to="/">Inicio</router-link>
        <router-link to="/about">Acerca de nosotros</router-link>
        <router-link to="/benchmark">Benchmarking</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavbarComponent'
};
</script>

<style scoped>
.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  font-size: 1.8rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-links a {
  color: #ecf0f1;
  text-decoration: none;
  margin-left: 25px;
  font-size: 1.1rem;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #42b983;
}

.router-link-exact-active {
  color: #42b983;
  font-weight: bold;
}

.nav-links a {
  color: #ecf0f1;
  text-decoration: none;
  margin-left: 25px;
  font-size: 1.1rem;
  transition: color 0.3s;
  padding: 5px 10px;
  border-radius: 4px;
}

.nav-links a:hover {
  background-color: rgba(255,255,255,0.1);
}

.router-link-exact-active {
  background-color: #42b983;
  font-weight: bold;
}
</style>