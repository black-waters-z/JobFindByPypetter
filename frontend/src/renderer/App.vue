<template>
  <div id="app">
    <nav>
      <router-link to="/">qq邮箱</router-link> |
      <router-link to="/liepin">猎聘</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup lang="ts">

</script>


<style lang="scss" scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>