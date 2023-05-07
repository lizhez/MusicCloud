<template>
  <div class="box">
    <div >
      <div class="name first">MyMusic</div>
      <div class="name second">Searching</div>
    </div>
    <div class="ipt">
      <div class="select">
        <el-dropdown trigger="click"
                     @command="Select">
          <span style="font-size: 18px;color: #828282;
                       margin-top:calc((100% - 30px) /2 - 3px);
                       margin-left:10px">
            {{select}}
            <el-icon>
              <ArrowDown />
            </el-icon>

          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="歌名">歌名</el-dropdown-item>
              <el-dropdown-item command="歌手">歌手</el-dropdown-item>
              <el-dropdown-item command="专辑">专辑</el-dropdown-item>
              <el-dropdown-item command="歌词">歌词</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>

      <input class="inp" placeholder="Enter vendor key here"
             v-model="quire"
             ref="ipt"
             @keydown="down()"
             @keyup="up(quire.length)">
      <div class="clear" v-if="isInput"
           @click="clear">
        <el-icon :size="20" color='#828282'>
          <CircleClose />
        </el-icon>
      </div>
    </div>

      <el-button class="bbtn" @click="ask">
        <el-icon><Search /></el-icon>
      </el-button>

    <div class="tag">
      <div style="font-size: small;
      color: rgba(217,247,248,0.75);
      margin-left: 5px;margin-bottom: 5px;
      position: relative">
        历史查询
        <div class="clearTag"
             @click="closeAll">
          <el-icon color='#828282' style="color: #d9f7f8">
            <Delete />
          </el-icon>
        </div>
      </div>
      <el-tag
          v-for="item in history"
          :key="item.label"
          type="info"
          closable
          size="small"
          effect="dark"
          :color="tagC"
          style="margin-left: 5px"
          @click="again(item)"
          @close="close(item)"
      >
        {{ item.label }}
      </el-tag>
    </div>

    <div class="detail">

      <el-collapse>
        <div class="results" v-for="(item,index) in tableData" :key="index">
          <el-collapse-item :name="index">
            <template #title>
              <div><h2 v-html="brightenKeyword(item.title, quire)" ></h2></div>
              <div>&nbsp;&nbsp;歌手：<span v-html="brightenKeyword(item.singer, quire)" ></span></div>
            </template>
            <div>专辑：《<span v-html="brightenKeyword(item.belong, quire)" />》</div>
            <el-button size="small" @click="playMusic(index)">
              <el-icon><CaretRight /></el-icon>
            </el-button>
            <el-button size="small" @click="seeImg(item.songid)">
              <el-icon><View /></el-icon>
            </el-button>
            <p v-html="brightenKeyword(item.contents, quire)" ></p>

          </el-collapse-item>
        </div>
      </el-collapse>
      <div class="pagination">
        <el-pagination
            @current-change="handleCurrentChange"
            :currentPage="pageNum"
            :page-size="5"
            layout="total, prev, pager, next"
            :total="total"
        >
        </el-pagination>
      </div>
    </div>

    <NeteaseCloudPlayForVue :url="url" :play="isplay"/>

    <el-dialog
        v-model="isShow"
        title="WordCloud"
        width="30%"
    >
      <img :src="imgURL" style="width: 100%;height: 200px">
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import {ArrowDown, CaretRight, CircleClose, Delete, Search, View} from "@element-plus/icons-vue";
import NeteaseCloudPlayForVue from "@/components/PlayMusic.vue";
export default {
  name: "SearchMusic",
  components:{
    View,
    NeteaseCloudPlayForVue,
    CaretRight,
    Search,
    Delete,
    ArrowDown,
    CircleClose
  },
  data(){
    return{
      isShow:false,
      isplay:true,
      imgURL:'',
      isInput:false,
      isFocus:false,
      select:'歌名',
      type:'title',
      quire:'',
      history:[],
      tagC:'rgba(180,180,180,0.58)',
      pageNum:1,
      pageSize:10,
      total:0,
      tableData:[],
      url:''
    }
  },
  mounted() {
    this.history=JSON.parse(localStorage.getItem("history"))
    this.load()
  },
  methods:{
    load(){
      axios.get("/api/musics",{
        params:{
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          search: this.quire,
        },
      }).then(
          res=>{
            console.log(res.data);
            this.tableData=res.data.data.records;
            this.total=res.data.data.total
          })
    },

    seeImg(songid){
      console.log(songid)
      this.imgURL = songid+'.jpg'
      this.isShow=true
    },

    ask(){

      axios.get("api/musics/search",{
        params:{
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          search: this.quire,
          type: this.type,
        }
      }).then(
          res=>{
            console.log(res.data);
            if(res.data.flag===true){
              console.log(res.data);
              this.tableData=res.data.data.records;
              this.total=res.data.data.total
              let temp={label:this.quire}
              let has=false
              for (let historyKey in this.history) {
                if(this.history[historyKey].label===this.quire){
                  has=true
                  break;
                }
              }
              if(!has){
                this.history.push(temp)
                localStorage.setItem("history",JSON.stringify(this.history))
                this.history=JSON.parse(localStorage.getItem("history"))
              }
            }else {
              this.$message({
                type: "error",
                message: "错误！"
              })
            }

          })
    },

    brightenKeyword(val, keyword) {
      val=val+""
      let keywordArr=keyword.split("");
      keywordArr.forEach(item=>{
        if(val.indexOf(item)!==-1&&item!==""){
          val=val.replace(new RegExp(item,'g'),
              '<font color="#52da52">'+item+'</font>')
        }
      })
      return val
    },


    down(){
      this.isFocus=true
    },
    up(l){
      if(l===0)
        this.isInput = false
      else if(l>0)
        this.isInput = true
    },
    clear(){
      this.$refs.ipt.focus()
      this.quire=''
      this.isInput = false
      this.isFocus=true
    },

    again(item){
      console.log(item)
      this.quire=item.label
      this.isInput = true
    },
    close(tag) {
      this.history.splice(this.history.indexOf(tag), 1)
      localStorage.removeItem("history")
      localStorage.setItem("history",JSON.stringify(this.history))
      this.history=JSON.parse(localStorage.getItem("history"))
    },
    closeAll() {
      this.history.splice(this.history.indexOf(this.history[0]), this.history.length)
      localStorage.removeItem("history")
      localStorage.setItem("history",JSON.stringify(this.history))
      this.history=JSON.parse(localStorage.getItem("history"))
    },

    Select(item){
      console.log('select',item)
      if(item==="歌名")
        this.type="name"
      else if(item==="歌手")
        this.type="singer"
      else if(item==="专辑")
        this.type="belong"
      else if(item==="歌词")
        this.type="contents"
      this.select=item
    },

    handleCurrentChange(pageNum) {
      this.pageNum=pageNum
      this.ask()
    },

    playMusic(t){
      console.log(this.tableData[t].loadurl)
      let u = this.tableData[t].loadurl.slice(6)
      console.log(u)
      this.url=u
      this.isplay=false
      // window.open(this.tableData[t].loadurl); //将新打的窗口对象，存储在变量mywin中
      // mywin.close();
    },
  }
}
</script>

<style scoped>
  .box{
    width: 100%;
    height: 200px;
    background-color: rgb(86, 124, 129);
    position: relative;
  }

  .name{
    position: absolute;
    font-size: 42px;
    color: #d9f7f8;
    font-family: '宋体';
    top:10%;

  }
  .first{
    left: 38%;
  }
  .second{
    left: 52%;
  }
  .img{
    position: absolute;
    left: 45%;
    top:6%
  }

  .ipt{
    position: absolute;
    width: 60%;
    height: 28%;
    border-radius: 10px;
    left: 20%;
    top: 45%;
    background-color: #E8E8E8B2;
  }

  .select{
    position: absolute;
    width: 10%;
    height: 100%;
    border-radius: 10px 0 0 10px;
  }
  .select:hover{
    background-color: rgba(180, 180, 180, 0.7);
  }

  .inp{
    outline:0;
    position: absolute;
    width: 89%;
    height: 70% ;
    border: none;
    font-size: 20px;
    left: 9.5%;
    top: 15%;
    padding-left: 5px;
    background-color: rgba(232, 232, 232, 0.0);
    color: rgb(82, 82, 82);
  }
  .inp:focus{
    background-color: rgb(255, 255, 255);
    color: rgb(0, 0, 0);
  }
  .clear{
    position: absolute;
    top: calc((100% - 20px)/2);
    right: 20px;
  }
  .bbtn{
    position: absolute;
    top: calc((100% + 20px)/2);
    right: 200px;
  }

  .tag{
    position: absolute;
    width: 60%;
    left: 20%;
    top: 74%;
  }
  .clearTag{
    position: absolute;
    top: 5px;
    right: 5px;
  }

  .detail{
    position: absolute;
    width: 100%;
    top: 100%;
  }

  .pagination{
    margin: 10px 0 5px 300px ;
  }
  .results{
    margin-top: 20px;
    width: 60%;
    margin-left: 20%;
  }

</style>