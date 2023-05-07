<template>

  <div>
<!--    <MusicSearch />-->

    <div class="nav">
      <router-link to="/">
        <el-button>
          <el-icon><House/></el-icon>
        </el-button>

      </router-link>
      <router-link to="/searching">
        <el-button style="margin-left: 10px">
          <el-icon><Search /></el-icon>
        </el-button>
      </router-link>

    </div>
    <div class="content">
      <router-view/>
    </div>
  </div>
</template>

<script>


import MusicSearch from "@/components/MusicSearch.vue";
import {House, Search} from "@element-plus/icons-vue";
export default {
  name: 'SearchWeb',
  components: {
    Search,
    House,
    // eslint-disable-next-line vue/no-unused-components
    MusicSearch,
  },
  data(){
    return{
    }
  }


}
</script>

<style scoped>
.nav{
  margin: 10px 700px;
}

</style>
