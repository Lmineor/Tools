<template>
  <div class="login">
    <nya-container :title=title>
      <Form label-position="left" :label-width="80" :model="info" :rules="ruleValidate" ref="info">
        <FormItem label="邮  箱：" class="form-item" prop="email">
          <Input v-model="info.email" autofocus></Input>
        </FormItem>
        <FormItem label="密 码：" class="form-item" prop="password">
            <Input v-model="info.password" type="password" @on-keyup.enter="login"></Input>
        </FormItem>
      </Form>
      <div class="nya-btn" id = "login" @click="login">登 录</div>
      <a href='/help'>忘记密码？</a>
      <div class="nya-btn" id="register" @click="register">注册</div>
    </nya-container>
  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'


export default {
  name: 'login',
  data () {
    return {
      title: '用户登录',
      email: '',
      password: '',
      isFocus: false,
      info: {
        email: '',
        password: '',
      },
      ruleValidate: {
        email: [
          {required: true, message: '邮箱不能为空', trigger: 'blur'},
          {type: 'email', message: '邮箱格式不正确', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '密码不能为空', trigger: 'blur'},
          { type: 'string', min: 6, max: 20, message: '密码长度6-20个字符', trigger: 'blur' },
        ],
      },
    }
  },
  methods: {
    login () {
      if ( this.info.email === '' || this.info.password === '') {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '邮箱或密码不能为空',
            timer: 1500,
        });
        return;
      };
      this.$axios.defaults.auth = {
        username: this.info.email,
        password: this.info.password,
      };
      this.$axios
        .get(envs.apiUrl + '/user/login')
         .then(re => {
          let token = re.data.token;
          let username = re.data.username;
          this.$store.state.user = username;
          this.$store.state.auth = token;
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
          this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '用户名或密码错误',
              timer: 1500,
          });
        });
    },
    register () {
      this.$router.push("/register")
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
    .form-item{
      font-size: 30px;
      margin-top: 20px;
      margin-bottom: 40px;
      letter-spacing: 1px;
      margin-right: 5px;
    }
    .nya-btn {
      font-size: 17px;
      font-weight: bold;
      text-align: center;
      margin-top:10px;
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
