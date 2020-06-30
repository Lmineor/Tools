<template>
  <div class="register">
    <nya-container :title=title>
      <Form label-position="left" :label-width="100" :model="info" :rules="ruleValidate" ref="info">
        <FormItem label="用户名：" prop="username">
          <Input v-model="info.username" autofocus></Input>
        </FormItem>
        <FormItem label="邮 箱：" prop="email">
          <Input v-model="info.email"></Input>
        </FormItem>
        <FormItem label="密 码：" prop="password1">
            <Input v-model="info.password1" type="password"></Input>
        </FormItem>
        <FormItem label="确认密码：" prop="password2">
            <Input v-model="info.password2" type="password" @on-keyup.enter="register"></Input>
        </FormItem>
      </Form>
      <div class="nya-btn" id="register" @click="register">注册</div><br>
      <span v-if="sent_email" style="font-size: x-small">邮件已经发送到注册的邮箱，点击链接激活账号<b>5分钟内有效</b></span>
      <br>
      <a v-if="sent_email" @click="register">没有收到？，点击重新发送，或瞅瞅垃圾箱里有没有？</a>
    </nya-container>

  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'


export default {
  name: 'register',
  data () {
    return {
      title: '注册',
      isFocus: false,
      sent_email: false,
      info: {
        username: '',
        email: '',
        password1: '',
        password2: '',
      },
      ruleValidate: {
        email: [
          {required: true, message: '邮箱不能为空', trigger: 'blur'},
          {type: 'email', message: '邮箱格式不正确', trigger: 'blur'}
        ],
        username: [
          {required: true, message: '用户名不能为空', trigger: 'blur'},
          { type: 'string', min: 1, max: 20, message: '长度1-20个字符', trigger: 'blur' },
        ],
        password1: [
          {required: true, message: '密码不能为空', trigger: 'blur'},
          { type: 'string', min: 6, max: 20, message: '密码长度6-20个字符', trigger: 'blur' },
        ],
        password2: [
          {required: true, message: '密码不能为空', trigger: 'blur'},
          { type: 'string', min: 6, max: 20, message: '密码长度6-20个字符', trigger: 'blur' },
        ],
      },
    }
  },
  methods: {
    register () {
      if (this.info.username === '' || this.info.email === '' || this.info.password1 === '') {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '用户名、邮箱、密码都不能为空',
            // title: err,
            timer: 3000,
        });
        return;
      };
      if (this.info.password1 != this.info.password2) {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '两次输入的密码不一致，请检查后重新输入',
            timer: 3000,
        });
        return;
      };
      this.$axios
        .post(
            envs.apiUrl + '/user/register',
            {
                username: this.info.username,
                email: this.info.email,
                password: this.info.password1,
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
