<template>
  <div class="register">
    <nya-container :title=title>
      <nya-input
        v-model="username"
        label="用户名"
        placeholder="用户名"
        autocomplete="off"
        autofocus
        fullwidth
      />
      <nya-input
        v-model="email"
        label="邮箱"
        placeholder="邮箱"
        autocomplete="off"
        autofocus
        fullwidth
      />
      <nya-input
        v-model="password1"
        label="密码"
        placeholder="位数大于等于6位小于等于32位"
        autocomplete="off"
        fullwidth
        type="password"
      />
      <nya-input
        v-model="password2"
        label="确认密码"
        placeholder="位数大于等于6位小于等于32位"
        autocomplete="off"
        fullwidth
        type="password"
        @keyup.enter="register"
      />
      <div class="nya-btn" id="register" @click="register">注册</div>
      <span v-if="sent_email" style="font-size: x-small">邮件已经发送到注册的邮箱，请尽快点击链接激活账号</span>
      <a v-if="sent_email" @click="register">没有收到？，点击重新发送，或瞅瞅垃圾箱里有没有？</a>
    </nya-container>

  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'
import {validEmail} from '@/utils/validate'


export default {
  name: 'register',
  data () {
    return {
      title: '注册',
      username: '',
      email: '',
      password1: '',
      password2: '',
      isFocus: false,
      sent_email: false
    }
  },
  methods: {
    register () {
      if (this.username === '' || this.email === '' || this.password1 === '') {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '用户名、邮箱、密码都不能为空',
            // title: err,
            timer: 3000,
        });
        return
      };
      if ( !validEmail(this.email)) {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '邮箱格式不正确',
            timer: 3000,
        });
        return
      };
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
            envs.apiUrl + '/user/register',
            {
                username: this.username,
                email: this.email,
                password: this.password1,
            },
        )
        .then(re => {
          if(re.data.code == 200) {
            this.sent_email = true;
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'success',
              title: '注册成功',
              timer: 1500,
            });
            // this.$router.push("/login") // 跳转到login页
          } else{
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: re.data.msg,
              timer: 3000,
            });
          }
        })
        .catch(err => {
            this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '注册失败',
            timer: 3000,
          });
        });
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .register {
    width: 100%;
    max-width: 400px;
    margin: 10px auto 0;
    .nya-btn {
      font-size: 17px;
      font-weight: bold;
      text-align: center;
      margin-top:15px;
      width: 100px;
    }
    #register{
      width: 100%;
    }
  }
</style>
