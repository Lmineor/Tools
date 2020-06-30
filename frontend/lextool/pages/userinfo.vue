<template>
  <div class="user-info">
    <nya-container :title=title>
      <Form label-position="left" :label-width="100" :model="info" :rules="ruleValidate" ref="info">
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="用户名：" prop="username">
                <Input v-model="info.username" style="width:50%;" @keyup.enter="update"></Input>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="邮箱：" style="margin-right: 5px;">
              <Input v-model="info.email" style="width:50%; font-weight: bold;" disabled></Input>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="单词书">
                <Select v-model="info.words_book" placeholder="类型" style="width:50%;">
                    <Option value="CET4">CET4</Option>
                    <Option value="CET6">CET6</Option>
                    <Option value="GRE">GRE</Option>
                    <Option value="TOEFL">TOEFL</Option>
                </Select>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="单词数量">
                <Select v-model="info.words_num" placeholder="数量" style="width:50%;">
                    <Option value="20">20</Option>
                    <Option value="50">50</Option>
                    <Option value="100">100</Option>
                    <Option value="200">200</Option>
                </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="修改密码">
              <i-switch v-model="modify"/>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem v-show="modify" label="密码" prop="password1">
                <Input v-model="info.password1" type="password" style="width:50%;"></Input>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem v-show="modify" label="确认密码" prop="password2">
                <Input v-model="info.password2" type="password" style="width:50%;" @on-keyup.enter="update"></Input>
            </FormItem>
          </Col>
        </Row>
      </Form>
      <div class="nya-btn" id="register" @click="update">更新信息</div>
      <div class="nya-btn" id="logout" @click="logout">退出登录</div>
    </nya-container>
    <nya-container title="提示" icon="volume-down-outline">
        <ul class="nya-list">
            <li>带*号的为必填项</li>
            <li>单词书更改后第二天才会生效哈~</li>
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
      modify : false,
      ruleValidate: {
        username: [
          {required: true, message: '用户名不能为空', trigger: 'change'},
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
      info: {
        username: '',
        email: '',
        words_book: 'CET4',
        words_num: 20,
        password1: '',
        password2: '',
      },
    }
  },
  mounted (){
    this.getUserInfo();
    this.username = Cookie.get('user');
    this.loading = false;
  },
  methods: {
    logout(){
      this.$axios
        .delete(
            envs.apiUrl + '/user/logout',
          {
            data:{
                username: this.info.username,
                email: this.info.email
            },
          }
        )
        .then(re => {
          if(re.data.code === 200) {
            let token = null;
            let username = null;
            this.$store.commit("SET_AUTH", token);
            this.$store.commit("SET_USER_IFO", username);
            Cookie.remove("auth");
            Cookie.remove("user");
            this.$router.push("/login");
          }
        })
        .catch(err => {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '注销失败',
              timer: 3000,
            });
          // this.$router.push("/")
        });
    },
    getUserInfo(){
      this.info.username = Cookie.get('user');
      this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      }
      this.$axios
        .get(
            envs.apiUrl + '/user/info',
        )
        .then(re => {
            this.info.email = re.data.email;
            this.info.words_book = re.data.words_book;
            this.info.words_num = re.data.words_num
          console.log(this.info.words_num)
        })
        .catch(err => {
          if (err.response.status === 401) {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '登录过期，请重新登录',
              timer: 3000,
            });
            this.$router.push("/login")
          }
          else {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '出了点问题，请重新登录',
              timer: 2000,
            });
            this.email = '';
            this.$router.push("/login") // 跳转到login页
          }
        });
    },
    update(){
      if (!this.info.username){
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '用户名不为空',
            timer: 3000,
        });
        return
      }
      if (this.info.password1 !== this.info.password2) {
        this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '两次输入的密码不一致，请检查后重新输入',
            timer: 3000,
        });
        return;
      };
      if (this.info.password1){
        if ( !((this.info.password1.length >= 6) && (this.info.password1.length <=32))) {
          this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '密码位数应大于等于6位小于等于32位',
              timer: 3000,
          });
          return
        };
      }
      this.$axios
        .post(
            envs.apiUrl + '/user/infoupdate',
            {
                username: this.info.username,
                email: this.info.email,
                password: this.info.password1,
                words_book : this.info.words_book,
                words_num: this.info.words_num,
            },
        )
        .then(re => {
          if(re.data.code === 200) {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'success',
              title: '更新成功，请重新登录',
              timer: 1500,
            });
            this.logout();
          } else{
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '未知错误，请重新登录试试',
              timer: 3000,
            });
            this.logout();
          }
        })
        .catch(err => {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '登录已过期，请重新登录',
              timer: 3000,
            });
          this.logout();
        });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .user-info {
    width: 100%;
    .nya-btn {
      position: relative;
      margin-top: 15px;
    }
    #logout{
      margin-left: 30px;
    }
  }
</style>
