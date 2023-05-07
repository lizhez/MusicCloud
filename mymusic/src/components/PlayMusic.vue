<template>
  <div>
    <div
        v-bind:class="NeteaseCloudPlayIframeClass"
        v-bind:style="NeteaseCloudPlayIframeStyle"
        @mousedown="NeteaseCloudPlayIframeMouseDownOrUp =  true"
        @mouseup="NeteaseCloudPlayIframeMouseDownOrUp = false"
        @touchend="NeteaseCloudPlayIframeMouseDownOrUp = false"
        @touchstart="NeteaseCloudPlayIframeMouseDownOrUp =  true"
        @touchmove.prevent.stop="NeteaseCloudPlayIframeForTouchClick($event)"
    >
      <el-row>
        <el-col :span="NeteaseIconSpan">
          <div
              v-bind:class="NeteaseCloudPlayIframeClassIcon"
              @mousedown="NeteaseShowClick"
              @mouseup="NeteaseIconUp = true"
          >
            <el-row>
              <i>
                <el-icon :pull="4" :span="1" v-if="NeteaseIconClass" @click="NeteaseIconClass=!NeteaseIconClass"><CaretRight /></el-icon>
                <el-icon :pull="4" :span="1" v-if="!NeteaseIconClass" @click="NeteaseIconClass=!NeteaseIconClass"><CaretLeft /></el-icon>
              </i>
            </el-row>
          </div>
        </el-col>
        <el-col :span="23">
          <div
              v-bind:class="NeteaseCloudPlayIframeDivClass"
              v-bind:style="NeteaseCloudPlayIframeDivStyle"
          >
            <iframe
                border="0"
                frameborder="no"
                height="86"
                marginheight="0"
                marginwidth="0"
                v-bind:src="url"
                v-bind:style="NeteaseCloudPlayIframeIframeStyle"
                style="background-color: rgba(130,130,130,0)"
                width="280"
            ></iframe>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
import {CaretLeft, CaretRight} from "@element-plus/icons-vue";

export default {
  name: 'PlayMusic',
  components: {CaretLeft, CaretRight},
  props: {
    url: String,
    play: Boolean,
  },
  data() {
    return {
      NeteaseCloudPlayIframeClass: "NeteaseCloudPlayIframe",
      NeteaseCloudPlayIframeStyle: "left:0;top:80%;",
      NeteaseCloudPlayIframeMouseDownOrUp: false,
      NeteaseCloudPlayIframeClassIcon: "NeteaseCloudPlayIframeIcon",
      NeteaseCloudPlayIframeDivStyle: "left:-270px;",
      NeteaseCloudPlayIframeWindowWidth: 0,
      NeteaseIconSpan: 1,
      NeteaseIconClass: this.play,
      NeteaseCloudPlayIframeDivClass: "NeteaseCloudPlayIframeDiv",
      NeteaseGPSLeftOrRight: true,
      NeteaseGPSTop: 0,
      NeteaseGPSLeft: 0,
      NeteaseIfMove: false,
      NeteaseIconUp: false,
      NeteaseLockIframeIframeStyle: true,
      NeteaseCloudPlayIframeIframeStyle:
          "mask-image: -webkit-linear-gradient(left, rgba(0, 0, 0, 0) 100%, rgba(0, 0, 0, 1) 0%);",
    };
  },
  methods: {
    NeteaseCloudPlayIframeClick(event) {
      var e = event || window.event;
      var ValueX = e.pageX || e.clientX + document.body.scroolLeft;
      var ValueY = e.pageY || e.clientY + document.body.scrollTop;
      var x = ValueX - 10;
      var y = ValueY - 45;
      if (this.NeteaseCloudPlayIframeMouseDownOrUp == true) {
        if (this.NeteaseCloudPlayIframeClass != "NeteaseCloudPlayIframe") {
          this.NeteaseCloudPlayIframeClass = "NeteaseCloudPlayIframe";
        }
        var HalfWindowWidth = this.NeteaseCloudPlayIframeWindowWidth / 2;
        var ToCenterLong = ValueX - HalfWindowWidth;
        if (ToCenterLong > 0) {
          this.NeteaseCloudPlayIframeStyle =
              "left:" + x + "px;" + "top:" + y + "px;";
          this.NeteaseGPSLeft = x;
          this.NeteaseGPSTop = y;
          if (ToCenterLong < 270) {
            if (this.NeteaseGPSLeftOrRight != false) {
              // this.NeteaseIconFlipClick();
              this.NeteaseGPSLeftOrRight = false;
              if (this.NeteaseLockIframeIframeStyle == false) {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv NeteaseCloudPlayIframeTransition";
                this.NeteaseCloudPlayIframeDivStyle = "left:-270px;";
              } else {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv";
                this.NeteaseCloudPlayIframeDivStyle = "left:0px;";
              }
            }
          }
        } else {
          this.NeteaseCloudPlayIframeStyle =
              "left:" + x + "px;" + "top:" + y + "px;";
          this.NeteaseGPSLeft = x;
          this.NeteaseGPSTop = y;
          if (HalfWindowWidth - ValueX < 270) {
            if (this.NeteaseGPSLeftOrRight != true) {
              // this.NeteaseIconFlipClick();
              this.NeteaseGPSLeftOrRight = true;
              if (this.NeteaseLockIframeIframeStyle == false) {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv NeteaseCloudPlayIframeTransition";
                this.NeteaseCloudPlayIframeDivStyle = "left:0px;";
              } else {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv";
                this.NeteaseCloudPlayIframeDivStyle = "left:-270px;";
              }
            }
          }
        }
        this.NeteaseIfMove = true;
      }
    },
    NeteaseCloudPlayIframeForTouchClick(event) {
      var ValueX = event.targetTouches[0].clientX;
      var ValueY = event.targetTouches[0].clientY;
      var x = ValueX - 10;
      var y = ValueY - 45;
      if (this.NeteaseCloudPlayIframeMouseDownOrUp == true) {
        if (this.NeteaseCloudPlayIframeClass != "NeteaseCloudPlayIframe") {
          this.NeteaseCloudPlayIframeClass = "NeteaseCloudPlayIframe";
        }
        var HalfWindowWidth = this.NeteaseCloudPlayIframeWindowWidth / 2;
        var ToCenterLong = ValueX - HalfWindowWidth;
        if (ToCenterLong > 0) {
          this.NeteaseCloudPlayIframeStyle =
              "left:" + x + "px;" + "top:" + y + "px;";
          this.NeteaseGPSLeft = x;
          this.NeteaseGPSTop = y;
          if (ToCenterLong < 270) {
            if (this.NeteaseGPSLeftOrRight != false) {
              // this.NeteaseIconFlipClick();
              this.NeteaseGPSLeftOrRight = false;
              if (this.NeteaseLockIframeIframeStyle == false) {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv NeteaseCloudPlayIframeTransition";
                this.NeteaseCloudPlayIframeDivStyle = "left:-270px;";
              } else {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv";
                this.NeteaseCloudPlayIframeDivStyle = "left:0px;";
              }
            }
          }
        } else {
          this.NeteaseCloudPlayIframeStyle =
              "left:" + x + "px;" + "top:" + y + "px;";
          this.NeteaseGPSLeft = x;
          this.NeteaseGPSTop = y;
          if (HalfWindowWidth - ValueX < 270) {
            if (this.NeteaseGPSLeftOrRight != true) {
              // this.NeteaseIconFlipClick();
              this.NeteaseGPSLeftOrRight = true;
              if (this.NeteaseLockIframeIframeStyle == false) {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv NeteaseCloudPlayIframeTransition";
                this.NeteaseCloudPlayIframeDivStyle = "left:0px;";
              } else {
                this.NeteaseCloudPlayIframeDivClass =
                    "NeteaseCloudPlayIframeDiv";
                this.NeteaseCloudPlayIframeDivStyle = "left:-270px;";
              }
            }
          }
        }
        this.NeteaseIfMove = true;
      }
    },
    NeteaseCloudPlayIframeWindowWidthClick() {
      this.NeteaseCloudPlayIframeWindowWidth = $(window).width();
    },
    NeteaseIconFlipClick() {
      if (this.NeteaseIconClass) {
        this.NeteaseIconClass = "right";
      } else {
        this.NeteaseIconClass = "left";
      }
    },
    NeteaseHelpToEdge() {
      if (this.NeteaseCloudPlayIframeMouseDownOrUp == false) {
        if (this.NeteaseIfMove == true) {
          if (
              this.NeteaseCloudPlayIframeClass !=
              "NeteaseCloudPlayIframe NeteaseCloudPlayIframeTransition"
          ) {
            this.NeteaseCloudPlayIframeClass =
                "NeteaseCloudPlayIframe NeteaseCloudPlayIframeTransition";
          }
          if (this.NeteaseGPSLeftOrRight == true) {
            this.NeteaseCloudPlayIframeStyle =
                "left:0;" + "top:" + this.NeteaseGPSTop + "px;";
          } else {
            this.NeteaseCloudPlayIframeStyle =
                "left:" +
                (this.NeteaseCloudPlayIframeWindowWidth - 100) +
                "px;" +
                "top:" +
                this.NeteaseGPSTop +
                "px;";
          }
        }
      }
    },
    NeteaseShowClick() {
      this.NeteaseIconUp = false;
      setTimeout(() => {
        if (this.NeteaseIconUp == true) {
          this.NeteaseCloudPlayIframeDivClass =
              "NeteaseCloudPlayIframeDiv NeteaseCloudPlayIframeDivTransition";
          let i;
          let x;
          let Show;
          let NotShow;
          if (this.NeteaseGPSLeftOrRight == true) {
            if (this.NeteaseCloudPlayIframeDivStyle != "left:-270px;") {
              // this.NeteaseIconFlipClick();
              this.NeteaseLockIframeIframeStyle = true;
              this.NeteaseCloudPlayIframeDivStyle = "left:-270px;";
              i = 0;
              NotShow = setInterval(() => {
                i++;
                x = i + 20;
                if (i == 100) {
                  x = 100;
                }
                this.NeteaseCloudPlayIframeIframeStyle =
                    "mask-image: -webkit-linear-gradient(left, rgba(0, 0, 0, 0) " +
                    i +
                    "%, rgba(0, 0, 0, 1) " +
                    x +
                    "%);";
                if (i == 100) {
                  clearInterval(NotShow);
                }
              }, 10);
            } else {
              // this.NeteaseIconFlipClick();
              this.NeteaseLockIframeIframeStyle = false;
              this.NeteaseCloudPlayIframeDivStyle = "left:0px;";
              i = 100;
              Show = setInterval(() => {
                i--;
                x = i + 20;
                if (i == 0) {
                  x = 0;
                }
                this.NeteaseCloudPlayIframeIframeStyle =
                    "mask-image: -webkit-linear-gradient(left, rgba(0, 0, 0, 0) " +
                    i +
                    "%, rgba(0, 0, 0, 1) " +
                    x +
                    "%);";
                if (i == 0) {
                  clearInterval(Show);
                }
              }, 10);
            }
          } else {
            if (this.NeteaseCloudPlayIframeDivStyle != "left:0px;") {
              // this.NeteaseIconFlipClick();
              this.NeteaseLockIframeIframeStyle = true;
              this.NeteaseCloudPlayIframeDivStyle = "left:0px;";
              i = 0;
              NotShow = setInterval(() => {
                i++;
                x = i + 20;
                if (i == 100) {
                  x = 100;
                }
                this.NeteaseCloudPlayIframeIframeStyle =
                    "mask-image: -webkit-linear-gradient(right, rgba(0, 0, 0, 0) " +
                    i +
                    "%, rgba(0, 0, 0, 1) " +
                    x +
                    "%);";
                if (i == 100) {
                  clearInterval(NotShow);
                }
              }, 10);
            } else {
              // this.NeteaseIconFlipClick();
              this.NeteaseLockIframeIframeStyle = false;
              this.NeteaseCloudPlayIframeDivStyle = "left:-270px;";
              i = 100;
              Show = setInterval(() => {
                i--;
                x = i + 20;
                if (i == 0) {
                  x = 0;
                }
                this.NeteaseCloudPlayIframeIframeStyle =
                    "mask-image: -webkit-linear-gradient(right, rgba(0, 0, 0, 0) " +
                    i +
                    "%, rgba(0, 0, 0, 1) " +
                    x +
                    "%);";
                if (i == 0) {
                  clearInterval(Show);
                }
              }, 10);
            }
          }
        }
      }, 200);
    },
  },
  mounted() {
    $(() => {
      $(window).mousemove(this.NeteaseCloudPlayIframeClick);
      this.NeteaseCloudPlayIframeWindowWidthClick();
      $(window).resize(this.NeteaseCloudPlayIframeWindowWidthClick);
      $(window).mouseup(this.NeteaseHelpToEdge);
      $(window).on("touchend", this.NeteaseHelpToEdge);
    });
  }
}
</script>
<style scoped>
.NeteaseCloudPlayIframe {
  position: fixed;
  width: 0;
}

.NeteaseCloudPlayIframeIcon {
  user-select: none;
  top: 10px;
  position: absolute;
  border-radius: 0 50% 50% 0;
  height: 66px;
  width: 18px;
  background-color: #cad0d7;
  z-index: 1;
}

.NeteaseCloudPlayIframeDiv {
  position: relative;
}

.NeteaseCloudPlayIframeIcon i {
  position: absolute;
  top: 12px;
  left: -2px;
  font-size: 25px;
  color: #1a4a72;
}

.NeteaseCloudPlayIframeTransition {
  transition: all 1s ease;
}

.NeteaseCloudPlayIframeDivTransition {
  transition: all 1s linear;
}
</style>
