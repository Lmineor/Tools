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
        v-model="password"
        label="密码"
        placeholder="密码"
        autocomplete="off"
        fullwidth
        type="password"
        @keyup.enter="login"
      />
      <div class="nya-btn" id="register" @click="register">注册</div>
    </nya-container>
    
  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'
import {validUsername} from '@/utils/validate'


export default {
  name: 'register',
  data () {
    return {
      title: '注册',
      username: '',
      email: '',
      password: '',
      isFocus: false
    }
  },
  methods: {
    register () {
      if (this.email === '' || this.password === '') {
        this.$swal({
                  toast: true,
                  position: 'top-end',
                  type: 'error',
                  title: 'error',
                  // title: err,
                  timer: 1500,
              });
        return
      }
      this.$axios
        .post(
            envs.apiUrl + '/auth/register',
            {
                username: this.username,
                email: this.email,
                password: this.password
            },
        )
        .then(re => {
          
          window.alert("注册成功");
          this.$router.push("/login") // 跳转到login页
        })
        .catch(err => {
            window.alert("用户名或密码错误");
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
    margin: 100px auto 0;
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
