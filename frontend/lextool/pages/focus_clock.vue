<template>
  <div class="main-clock">
    <nya-container :title=title>
      <fullscreen :fullscreen.sync="fullscreen" background="#111">
        <div @click="toggle" title="全屏" class="button">
          <Icon type="ios-move" size="30"/>
        </div>
        <div v-if="fullscreen" class="time-area" style="color: #ffffff; margin-top: 10%;">
          <div class="YMD">
          {{currentYMD}}
          </div>
          <div class="time">
            {{currentTime}}
          </div>
          <div class="tip">{{tip}}</div>
        </div>
        <div v-else class="time-area" style="color: #111111">
          <div class="YMD">
          {{currentYMD}}
          </div>
          <div class="time">
            {{currentTime}}
          </div>
        </div>
      </fullscreen>
    </nya-container>
  </div>

</template>

<script>
import envs from '../env'


export default {
  name: 'admin',
  data () {
    return {
      title: '专注时钟',
      currentYMD: '',
      currentTime: '',
      fullscreen: false,
      tip:'保持专注'
    }
  },
  mounted() {
    setInterval( ()=>{
            this.getTime();
    },1000)

  },
  methods: {
    toggle () {
        this.fullscreen = !this.fullscreen
    },
    getTime:function(){;
      let yy = new Date().getFullYear();
      let mm = new Date().getMonth()+1;
      let dd = new Date().getDate();
      let hh = new Date().getHours();
      let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
      let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
      this.currentYMD = yy + '-' + mm + '-' + dd;
      this.currentTime = hh+':'+mf+':'+ss;
    },
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .main-clock{
    font-family: "Times New Roman";
    text-align: center;
    .button{
      float: right;
    }
    .time-area{
      /*color:#111111;*/
      .YMD {
       font-size: 50px;
      }
      .time{
        margin-top: 50px;
        font-size: 170px;
      }
      .tip{
        font-size: 30px;
        font-family: 楷体;
        margin-top: 60px;
      }
    }
  }
</style>
