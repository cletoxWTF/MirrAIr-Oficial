<template>
  <navbar-component-vue>
  </navbar-component-vue>
  <router-view/>

  <footer-component-vue>
  </footer-component-vue>

</template>

<script>
  import NavbarComponentVue from './components/NavbarComponent.vue'
  import FooterComponentVue from './components/FooterComponent.vue'
  
  export default{
    name:'App',
    components:{
      NavbarComponentVue,
      FooterComponentVue
    }
  }
</script>

<style>

</style>
