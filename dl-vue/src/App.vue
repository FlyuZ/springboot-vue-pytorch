
<template>
  <nav-menu />
  <div class="navContent">
    <router-view></router-view>
  </div>
</template>

<script>
import NavMenu from "./views/NavMenu.vue";
export default {
  components: { NavMenu },
};
</script>

