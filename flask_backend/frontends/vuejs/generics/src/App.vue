 <!-- App.vue -->
<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <AppFizzle msg="Welcome to AppFizzle!"/>
</template>

<script>
import AppFizzle from './components/AppFizzle.vue'

export default {
  name: 'App',
  components: {
    AppFizzle
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
