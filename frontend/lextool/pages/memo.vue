<template>
  <div class="memo">
    <nya-container :title=title>
      <Input
        v-model="memo"
        type="textarea"
        placeholder="Enter something..."
        class="textarea"
        :autosize="{minRows: rows,maxRows: rows}"
      />
      <div class="nya-btn" @click="savememo">保存</div>
    </nya-container>

  </div>
</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'
import {validUsername} from '@/utils/validate'


export default {
  middleware: 'authenticated', // 需要登录
  name: 'memo',
  data () {
    return {
      rows: 23,
      memo: '',
      title: '便签',
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
      this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      }
      this.$axios
        .get(
            envs.apiUrl + '/user/memo',
        )
        .then(re => {
            this.memo = re.data.memo;
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
              title: '登录过期，请重新登录',
              timer: 2000,
            });
            this.$router.push("/login")
          }
        });
    },
    savememo() {
      this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      }
      this.$axios
        .post(
            envs.apiUrl + '/user/memo/update',
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
