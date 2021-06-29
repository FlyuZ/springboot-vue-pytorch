<template>
  <div class="test" style="width: 100%; height: 600px">
    <el-row>
      <el-button
        id="init"
        type="primary"
        round
        @click="initdl()"
        :loading="loadingflag"
      >
        初始化模型</el-button
      >
      <el-switch v-model="value1" inactive-text="播放" active-text="暂停">
      </el-switch>
    </el-row>
    <div
      style="
        width: 90%;
        height: 282px;
        float: left;
        margin-left: 5%;
        margin-top: 1%;
      "
    >
      <canvas
        id="can"
        width="640"
        height="360"
        style="background-color: #cccccc"
      ></canvas>
    </div>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.baseURL = "/api";
axios.defaults.headers["X-Requested-With"] = "XMLHttpRequest";
axios.defaults.headers.post["Content-Type"] = "application/json;charset=UTF-8";
export default {
  name: "test",
  data() {
    return {
      value1: false,
      base64img: "",
      loadingflag: false,
    };
  },
  mounted: function () {
    // 页面加载时触发
    this.drawfame();
  },
  watch: {
    // 监听开关的值是否改变
    value1(value) {
      let _this = this;
      if (value === true) {
        _this.timer = setInterval(function () {
          // 构建下一张图片地址
          _this.getimg()
          // console.log(this.base64img)
          // 重新绘制
          _this.drawfame()
        }, 50);
      } else {
        window.clearInterval(_this.timer);
      }
    },
  },
  methods: {
    drawfame() {
      var can = document.getElementById("can")
      var cxt = can.getContext("2d")
      var img = new Image()
      img.src = this.base64img
      img.onload = function () {
        cxt.drawImage(img, 0, 0, 640, 360);
      };
    },
    getimg() {
      // GET
      axios.get("/getimg").then((response) => {
        this.base64img = "data:image/jpg;base64," + response.data;
        console.log(this.base64img.length)
      });
    },
    initdl() {
      this.loadingflag = true;
      axios.get("/initdl").then((response) => {
        this.res = response.data;
        if (this.res == "success") {
          this.loadingflag = false;
          console.log("init success");
        }
      });
    },
  },
};
</script>

<style>
</style>