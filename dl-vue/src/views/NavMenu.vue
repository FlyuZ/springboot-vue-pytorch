<template>
  <el-menu
    :default-active="path"
    router
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item index="/Home">首页</el-menu-item>
    <el-menu-item index="/Live">监控页</el-menu-item>
    <el-menu-item index="/DL">追踪页</el-menu-item>
  </el-menu>
  <div class="line"></div>
</template>

<script>
export default {
  created() {
    this.onRouteChanged();
  },
  watch: {
    $route: "onRouteChanged",
  },
  methods: {
    onRouteChanged() {
      let that = this;
      that.path = that.$route.path;
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>