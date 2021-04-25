<template>
  <div class="main-clock">
    <nya-container :title=title>
      <fullscreen :fullscreen.sync="fullscreen" background="#111">
        <div v-if="fullscreen" class="time-area" style="color: #ffffff; margin-top: 7%;text-align: center;">
          <div v-if="model">
            <div class="YMD" style="font-size: 50px;">
            {{currentYMD}}
            </div>
            <div style="margin-top: 50px;">
              <span style="font-size: 170px;">{{m}}</span>
              <span style="font-size: 30px;"> 分 </span>
              <span style="font-size: 170px;">{{s}}</span>
              <span style="font-size: 30px;"> 秒 </span>
            </div>
          </div>
          <div v-else>
            <div class="YMD" style="font-size: 50px;">
            {{currentYMD}}
            </div>
            <div class="time" style="margin-top: 50px;font-size: 170px;">
              {{currentTime}}
            </div>
          </div>
          <div class="tip" style="font-size: 30px;font-family: 楷体;margin-top: 60px;">{{tip}}</div>
        </div>
        <div v-else class="config-area" style="color: #111111; margin-top: 3%;">
          <Card class="time-card">
            <p slot="title">
<!--              <Icon type="ios-calendar-outline" />-->
              当前时间：{{currentYMD}} {{currentTime}}
            </p>
<!--            <ul>-->
<!--              <h2 style="font-size: 15px;">选择想要的功能（可不选）：</h2>-->
<!--                <RadioGroup v-model="model" >-->
<!--                  <Radio label="" class="radio-group">-->
<!--                      <span>不选了</span>-->
<!--                  </Radio>-->
<!--                  <Radio label="countdown" class="radio-group">-->
<!--                      <span>倒计时</span>-->
<!--                  </Radio>-->
<!--                  <Radio label="tomato" stle="margin-left:5px;" class="radio-group">-->
<!--                      <span>番茄时钟</span>-->
<!--                  </Radio>-->
<!--              </RadioGroup>-->

<!--            </ul>-->
<!--            <ul style="margin-top: 10px;" v-if="model === 'countdown'">-->
<!--              <span>倒计时：</span>-->
<!--              <Select v-model="timer"  style="width:100px">-->
<!--                  <Option v-for="item in intervals" :value="item">{{ item }}</Option>-->
<!--              </Select>-->
<!--              <span>分钟</span>-->
<!--&lt;!&ndash;              <Dropdown v-if="model === 'countdown'" class="drop-down">&ndash;&gt;-->
<!--&lt;!&ndash;                <a>&ndash;&gt;-->
<!--&lt;!&ndash;                    选择时间&ndash;&gt;-->
<!--&lt;!&ndash;                    <Icon type="ios-arrow-down"></Icon>&ndash;&gt;-->
<!--&lt;!&ndash;                </a>&ndash;&gt;-->
<!--&lt;!&ndash;                <DropdownMenu slot="list">&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>1</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>2</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>3</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>4</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>5</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>10</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>15</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>20</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>25</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                  <DropdownItem>30</DropdownItem>&ndash;&gt;-->
<!--&lt;!&ndash;                </DropdownMenu>&ndash;&gt;-->
<!--&lt;!&ndash;              </Dropdown>&ndash;&gt;-->
<!--            </ul>-->
          </Card>
          <Card class="slogan-card" style="margin-top: 20px">
            <p slot="title" style="font-weight: bold;font-size: 19px">
              Slogan
            </p>
            <ul>
              <span>
                <nya-input v-model.trim="tip" fullwidth autofocus/>
              </span>
            </ul>
          </Card>
          <div class="nya-btn" @click="toggle" style="float: left;margin-top: 20px">
            开始
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
      timer: 1,
      intervals:[1,2,3,4,5,10,15,30,60],
      tip:'保持专注',
      model:'',
      timer_s: 0,
      m: 1,
      s: 0,
    }
  },
  mounted() {
    setInterval( ()=>{
            this.getTime();
    },1000)

  },
  methods: {
    toggle () {
      this.timer_s = this.timer * 60;
      // if(this.model === 'countdown'){
      //   this.set_timmer();
      // }
      this.fullscreen = !this.fullscreen
    },
    set_timmer(){
      let count = 0;
      this.m = this.timer - 1
      setInterval( ()=>{
        this.timer_s = this.timer_s -1;
        count = count + 1;
        if(count === 59){
          this.m = Math.floor(this.timer_s / 60);
        }
        this.s = this.timer_s - this.m*60
      },1000);
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
      font-size: 17px;
    }
    .time-area{
      display: table;
      width: 100%;
      .time{

      }
      .tip{

      }
    }
    .config-area{
      display: table;
      width: 100%;
      .radio-group{
        font-size: 15px;
      }
      .drop-down{
        margin-right: 40%;
        font-size: 15px;
      }
    }
  }
</style>
