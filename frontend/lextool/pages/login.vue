<template>
  <div class="login">
    <nya-container title="用户登录">
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
import envs from '../env'
import {validUsername} from '@/utils/validate'
import Cookie from 'js-cookie'; 

export default {
  name: 'login',
  data () {
    return {
      email: '',
      password: '',
      isFocus: false
    }
  },
  methods: {
    login () {
      if (this.email === '' || this.password === '') {
        window.alert("用户名或密码不能为空");
        return
      }
      this.$axios
        .post(
            envs.apiUrl + '/login',
            {
                email: this.email,
                password: this.password
            },
        )
        .then(re => {
            this.$store.commit('SET_USER', this.username);
            Cookie.set('Authorization', re.data.token)
            // localStorage.setItem('Authorization', re.data.token)
            // localStorage.setItem('username', this.username)
            this.$router.push("/") // 跳转到首页
        })
        .catch(err => {
            window.alert("用户名或密码错误");
        });
    },
    register () {
      if (this.email === '' || this.password === '') {
        window.alert("用户名或密码不能为空");
        return
      }
      this.$axios
        .post(
            envs.apiUrl + '/register',
            {
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
  // mounted() {
  //   if (this.email === '') {
  //     this.$refs.email.focus()
  //   } else if (this.password === '') {
  //     this.$refs.password.focus()
  //   }
  // },
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
