<template>
  <div class="memo">
    <nya-container :title=title>
      <!-- <nya-input
        type="textarea"
      /> -->
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
      memo: '造吧',
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
            envs.apiUrl + '/api/auth/usermemo',
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
            envs.apiUrl + '/api/auth/saveusermemo',
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
    background:url(http://www.lanrentuku.com/down/js/images/12450456760.gif) no-repeat right top;
    .textarea{
      height: 500px;
      text-overflow: ellipsis;
      background-color: #ffffff;
      font-size: 15px;
    }
    .nya-btn {
      position: relative;
      margin-top: 15px;
    }
  }
</style>
