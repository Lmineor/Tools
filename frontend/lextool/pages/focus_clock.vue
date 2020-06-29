<template>
  <div class="main-clock">
    <nya-container :title=title>
      <fullscreen :fullscreen.sync="fullscreen" background="#111">
        <div v-if="fullscreen" class="time-area" style="color: #ffffff; margin-top: 7%;text-align: center;">
          <div class="YMD" style="font-size: 50px;">
          {{currentYMD}}
          </div>
          <div class="time" style="margin-top: 50px;font-size: 170px;">
            {{currentTime}}
          </div>
          <div class="tip" style="font-size: 30px;font-family: 楷体;margin-top: 60px;">{{tip}}</div>
        </div>
        <div v-else class="time-area" style="color: #111111; margin-top: 3%;">
          <Card class="time-card">
            <p slot="title">
              <Icon type="ios-calendar-outline" />
              日期：{{currentYMD}}
            </p>
            <ul>
              <span>
                <Icon type="ios-clock-outline" />
                当前时间：{{currentTime}}
              </span>
            </ul>
<!--            <ul style="margin-top: 10px;">-->
<!--              倒计时：<i-switch v-model="countdown"/>-->
<!--              <Dropdown v-if="countdown">-->
<!--                <a href="javascript:void(0)">-->
<!--                    选择时间-->
<!--                    <Icon type="ios-arrow-down"></Icon>-->
<!--                </a>-->
<!--                <DropdownMenu slot="list">-->
<!--                  <DropdownItem>1</DropdownItem>-->
<!--                  <DropdownItem>1</DropdownItem>-->
<!--                  <DropdownItem>3</DropdownItem>-->
<!--                  <DropdownItem>4</DropdownItem>-->
<!--                  <DropdownItem>5</DropdownItem>-->
<!--                  <DropdownItem>10</DropdownItem>-->
<!--                  <DropdownItem>15</DropdownItem>-->
<!--                  <DropdownItem>20</DropdownItem>-->
<!--                  <DropdownItem>25</DropdownItem>-->
<!--                  <DropdownItem>30</DropdownItem>-->
<!--                </DropdownMenu>-->
<!--              </Dropdown>-->
<!--            </ul>-->
          </Card>
          <Card class="time-card" style="margin-top: 20px">
            <p slot="title" style="font-weight: bold;font-size: 20px">
              Slogan
            </p>
            <ul>
              <span>
                <nya-input v-model.trim="tip" fullwidth autofocus/>
              </span>
            </ul>
          </Card>
          <div class="nya-btn" @click="toggle" style="float: left;margin-top: 20px">
<!--                <Icon type="ios-move" size="20"/>-->
            Go
        </div>
        </div>

      </fullscreen>
    </nya-container>

    <nya-container title="提示" icon="volume-down-outline">
            <ul class="nya-list">
                <li>全屏模式使用效果更佳奥~</li>
            </ul>
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
      countdown:false,
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
    .time-card{

    }
    .time-area{
      display: table;
      width: 100%;
      .time{

      }
      .tip{

      }
    }
  }
</style>
