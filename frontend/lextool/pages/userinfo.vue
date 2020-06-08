<template>
  <div class="user-info">
    <nya-container :title=title>
      <Form :model="formLeft" label-position="left" :label-width="70">
        <FormItem label="用户名*">
            <Input v-model="username" style="width:30%;" @keyup.enter="update"></Input>
        </FormItem>
        <FormItem label="邮箱">
            <span style="width:30%;">{{email}}</span>
        </FormItem>
        <FormItem v-if="modify" label="密码">
            <Input v-model="password1" type="password" style="width:30%;"></Input>
            <span style="color:rgb(255, 0, 0);">位数大于等于6位小于等于32位</span>
        </FormItem>
        <FormItem v-if="modify" label="确认密码">
            <Input v-model="password2" type="password" style="width:30%;" @keyup.enter="update"></Input>
            <span style="color:rgb(255, 0, 0);">位数大于等于6位小于等于32位</span>
        </FormItem>
    </Form>
    <div class="nya-btn" id="register" @click="update">更新信息</div>
    </nya-container>
    <nya-container title="提示" icon="volume-down-outline">
        <ul class="nya-list">
            <li>带*号的为必填项</li>
            <li>若不修改密码，置空即可</li>
            <li>有问题，联系我<a href="mailto:luohai2233@163.com">luohai2233@163.com</a></li>
        </ul>
    </nya-container>
  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'


export default {
  middleware: 'authenticated', // 需要登录
  name: 'memo',
  data () {
    return {
      title: '个人信息',
      username: '',
      email: '',
      modify : true,
      password1: '',
      password2: '',
    }
  },
  mounted (){
    this.getUserInfo();
    this.username = Cookie.get('user');
    this.loading = false;
  },
  methods: {
    getUserInfo(){
      this.username = Cookie.get('user');
      this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      }
      this.$axios
        .get(
            envs.apiUrl + '/user/userinfo',
            {withCredentials: true}
        )
        .then(re => {
            this.email = re.data.email;
        })
        .catch(err => {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '出了点问题，请稍候再试',
              timer: 2000,
            });
            this.email = '';
        });
    },
    update(){
      if (!this.username){
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '用户名不为空',
            timer: 3000,
        });
        return
      }
      if (this.password1 != this.password2) {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '两次输入的密码不一致，请检查后重新输入',
            timer: 3000,
        });
        return
      };
      if ( !((this.password1.length >= 6) && (this.password1.length <=32))) {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '密码位数应大于等于6位小于等于32位',
            timer: 3000,
        });
        return
      };
      this.$axios
        .post(
            envs.apiUrl + '/user/update',
            {
                username: this.username,
                email: this.email,
                password: this.password1
            },
        )
        .then(re => {
          if(re.data.code == 200) {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'success',
              title: '更新成功，请重新登录',
              timer: 1500,
            });
            this.$router.push("/login") // 跳转到login页
          } else{
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '出了点问题，请稍后再试',
              timer: 3000,
            });
          }
        })
        .catch(err => {
            this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '未知错误',
            timer: 3000,
          });
        });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .memo {
    width: 100%;
    .textarea{
      height: 500px;
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
