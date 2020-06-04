<template>
  <div class="todo">
    <nya-container :title=title>
      <Input v-model="todo" class="contend">
        
        <Radio slot="append">
            <span>完成</span>
        </Radio>
      </Input>
      <TimePicker :steps="[1, 15, 15]" placeholder="Select time" style="width: 112px"></TimePicker>
      <div class="nya-btn" @click="savememo">保存</div>
    </nya-container>

  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'
import {validUsername} from '@/utils/validate'


export default {
  // middleware: 'authenticated', // 需要登录
  name: 'memo',
  data () {
    return {
      rows: 23,
      todo: '造吧',
      title: 'ToDo',
      email: '',
      password: '',
      isFocus: false,
      loading: true,
      user: ''
    }
  },
  mounted (){
    this.getmemo();
    // setInterval(() => {
    //     this.savememo();//保存表单信息的操作
    //   },20000)
    this.loading = false;
  },
  methods: {
    getmemo(){
      this.user = Cookie.get('user');
      this.$swal({
          toast: false,
          position: 'center',
          title: '你好: ' + this.user,
          timer: 1500,
        });
      this.$axios.defaults.auth = {
                username: Cookie.get('auth'),
                password: ''
      }
      this.$axios
        .get(
            envs.apiUrl + '/user/usermemo',
            {withCredentials: true}
        )
        .then(re => {
            this.memo = re.data.memo;
        })
        .catch(err => {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '出了点问题，请稍候再试',
              timer: 2000,
            });
            this.memo = '';
        });
    },
    savememo() {
      this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      }
      this.$axios
        .post(
            envs.apiUrl + '/user/saveusermemo',
            {
                username: this.user,
                memo: this.memo,
            },
        )
        .then(re => {
          this.$swal({
              toast: true,
              position: 'top-end',
              type: 'success',
              title: '保存成功',
              timer: 1500,
            });
        })
        .catch(err => {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '出了点问题，请稍候再试',
              timer: 2000,
            });
            this.memo = '';
        });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .todo {
    width: 100%;
    .contend{
      width: 60%;
      text-overflow: ellipsis;
      font-size: 15px;
      border-style: none; 
    }
    .nya-btn {
      position: relative;
      margin-top: 15px;
    }
  }
</style>
