<template>
<div>
  <div style="background-color: rgb(86, 124, 129);color: #d9f7f8;padding:10px 600px;font-size: 35px;line-height: 100px;font-family: 宋体;">THE DATA OF SONGS</div>
  <div style="height:600px;padding: 20px 140px;">
    <div class="data" id="singer"></div>
    <div class="data" id="belong" style="margin-left: 35px"></div>
<!--    <div class="data" id="travel"></div>-->
  </div>
  <div style="background-color: rgb(86, 124, 129);color: #d9f7f8;margin: 30px 0;padding:10px 550px;font-size: 35px;line-height: 100px;font-family: 宋体;">THE WORDCOULD OF SONGS</div>
  <div style="padding:10px 140px;margin-bottom: 100px">
    <div style="height: 100px;width: 250px;float: left">
      <el-row class="tac">
        <el-col>
          <h4 class="mb-2">Searching For</h4>
          <el-menu
              class="el-menu-vertical-demo"
              @open="handleOpen"
              @close="handleClose"
          >
            <el-sub-menu index="1">
              <template #title>
                <el-icon><User /></el-icon>
                <span>Singer</span>
              </template>
              <el-scrollbar height="150px">
                <div v-for="(item,index) in Users" :key="index">
                  <el-menu-item :index='"1-"+(index+1)' @click="textcould(item.name)">{{item.name}}</el-menu-item>
                </div>
              </el-scrollbar>
            </el-sub-menu>
            <el-sub-menu index="2">
              <template #title>
                <el-icon><FolderOpened /></el-icon>
                <span>Belong</span>
              </template>
              <el-scrollbar height="150px">
                <div v-for="(item,index) in Belongs" :key="index">
                  <el-menu-item :index='"2-"+(index+1)' @click="textcould(item.name)">{{item.name}}</el-menu-item>
                </div>
              </el-scrollbar>
            </el-sub-menu>
          </el-menu>
        </el-col>
      </el-row>
    </div>
    <div style="width: 900px;height: 500px;float: left;margin-left: 30px;padding: 20px 200px">
      <img :src="imgURL" style="width: 100%;height: 100%">
    </div>
  </div>
<!--  <el-button @click="textcould(28457932)"></el-button>-->
</div>
</template>




<script>
import * as echarts from 'echarts';
import axios from "axios";
import {FolderOpened, User} from "@element-plus/icons-vue";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Main",
  components: {User, FolderOpened},
  data(){
    return{
      imgURL:'mymusic.jpg',
      Users:[],
      Belongs:[],
      option1: {
        title: {
          text: "最喜爱歌手 TOP10",
          subtext: '收藏歌曲数量',
          // left:'center'

        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} 首({d}%)'
        },
        legend: {
          top: 'bottom'
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        series: [
          {
            top:'10%',
            bottom:'10%',
            name: '最喜爱歌手 TOP10',
            type: 'pie',
            radius: [30, 250],
            center: ['50%', '50%'],

            roseType: 'area',
            itemStyle: {
              borderRadius: 5,
            },
            data: [],

          }
        ]
      },
      option2:{
        title: {
          text: "最喜爱专辑 TOP10",
          subtext: '专辑歌曲数量',
        },
        tooltip: {},
        xAxis: {
          axisLabel: {
            interval:0,
            rotate:28
          },
          data: []
        },
        yAxis: {},
        series: [
          {
            top:'20%',
            bottom:'20%',
            name: "专辑歌曲数量",
            type: "bar",
            data: [],
            itemStyle: {
              normal: {
                //这里是重点
                color: function(params) {
                  //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
                  var colorList = ['#2e5e67','#2f4554', '#61a0a8',
                    '#334d6c', '#91c7ae','#749f83', '#54577c',
                    '#445246', '#486945', '#1a4a72'];
                  return colorList[params.dataIndex]
                }
              }
            }
          },
        ],
      },
    }
  },
  mounted() {
    this.load()
  },
  methods:{
    load(){
      let myChart1 = echarts.init(document.getElementById('singer'));
      document.getElementById('singer').setAttribute('_echarts_instance_', '')
      myChart1.setOption(this.option1)
      axios.get("/api/musics/singer").then(
          res=>{
            console.log("singer: ",res.data.data)
            this.Users=res.data.data
            console.log("user",this.Users)
            myChart1.resize()
            myChart1.setOption({
              series: [
                {
                  data:res.data.data
                }
              ]
            })
          }
      )
      let myChart2 = echarts.init(document.getElementById('belong'));
      document.getElementById('belong').setAttribute('_echarts_instance_', '')
      myChart2.setOption(this.option2)
      axios.get("/api/musics/belong").then(
          res=>{
            console.log("belong: ",res.data.data)
            this.Belongs = res.data.data
            console.log("belongsss",this.Belongs)

            let names=[],values=[]
            for (const k in res.data.data) {
              names[k]=res.data.data[k].name
              values[k]=res.data.data[k].value

            }
            myChart2.setOption({
              xAxis: {
                data: names
              },
              series: [
                {
                  data: values
                },
              ],
            })
          }
      )
    },

    textcould(name){
      console.log(name)
      this.imgURL=name+'.jpg'
    },
    handleOpen(key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose(key, keyPath){
      console.log(key, keyPath)
    },
  },
}
</script>

<style scoped>
.data{
  display:inline-block;
  width: 600px;
  height:600px;
  /*margin-right:10px;*/
  /*padding: 10px;*/
}
</style>