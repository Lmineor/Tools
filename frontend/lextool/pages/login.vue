<template>
  <div class="login">
    <nya-container :title=title>
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
      <div class="nya-btn" id = "login" @click="login">登 录</div>
      <div class="nya-btn" id="register" @click="register">注册</div>
    </nya-container>
    
  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'
import {validEmail} from '@/utils/validate'


export default {
  name: 'login',
  data () {
    return {
      title: '用户登录',
      email: '',
      password: '',
      isFocus: false
    }
  },
  methods: {
    login () {
      if ( this.email === '' || this.password === '') {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '邮箱或密码不能为空',
            timer: 1500,
        });
        return
      }
      if ( !validEmail(this.email)) {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '邮箱格式不正确',
            timer: 1500,
        });
        return
      }
       this.$axios.defaults.auth = {
                username: this.email,
                password: this.password,
            }
      this.$axios
        .get(envs.apiUrl + '/auth/login')
         .then(re => {
          let token = re.data.token;
          let username = re.data.username;
          this.$store.commit("SET_AUTH", token);
          this.$store.commit("SET_USER_IFO", username);
          Cookie.set("auth", token);
          Cookie.set("user", username);
          this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'success',
                    title: '登录成功',
                    timer: 2000,
                });
          this.$router.push("/") // 跳转到首页
        })
        .catch(err => {
          console.log(err);
          this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '用户名或密码错误',
              // title: err,
              timer: 1500,
          });
        });
    },
    register () {
      this.$router.push("/register") // 跳转到首页
    }
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .login {
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
    #login{
      margin-left: 0;
    }
    #register{
      float: right;
    }
  }
</style>
