<template>
  <div class="admin">
    <nya-container :title=title>
      <div>
          <table class="nya-table">
              <tr>
                  <th>用户名</th>
                  <th>邮箱</th>
                  <th>单词书</th>
                  <th>密码</th>
                  <th>危险操作</th>
              </tr>
              <tr v-for="(item, index) in users" :key="index">
                  <td>{{ item.username }}</td>
                  <td>{{item.email}}</td>
                  <td>{{item.wordbook}}</td>
                  <td>
                    <Button type="primary" @click="update">初始化密码</Button>
                  </td>
                  <td>
                    <Button type="warning" @click="delete_user">删除用户</Button>
                  </td>
              </tr>
          </table>
      </div>
    </nya-container></div>

</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'
import {validEmail} from '@/utils/validate'


export default {
  middleware: 'authenticated', // 需要登录
  name: 'admin',
  data () {
    return {
      title: '用户管理',
      username: '',
      email: '',
      password: '',
      users: Array
    }
  },
  mounted (){
        this.getUsers()
    },
  methods: {
    getUsers(){
      this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      };
      this.$store.commit('SET_STORE', {
          key: 'globalLoading',
          value: true
      });
      this.$axios
        .get(
          envs.apiUrl + '/user/users',
          // {withCredentials: true}
        )
        .then(re => {
          if(re.data){this.users = re.data;}
          else{
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'error',
              title: '你没有权限',
              timer: 3000,
            });
            this.$router.push("/"); // 跳转到首页
          }
          this.$store.commit('SET_STORE', {
            key: 'globalLoading',
            value: false
          });
        })
        .catch(err => {
          this.$store.commit('SET_STORE', {
            key: 'globalLoading',
            value: false
          });
          this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '登录过期，请重新登录',
            timer: 3000,
          });
          this.$router.push("/login")
        })
    },
    update(){
      this.$axios
        .post(
          envs.apiUrl + '/user/update',
          {
            username: this.username,
            email: this.email,
            password: '123456abc'
          },
        )
        .then(re => {
          if (re.data.code == 200) {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'success',
              title: '操作成功',
              timer: 1500,
            });
          }
        })
        .catch(err => {
          this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '操作失败，请排查',
            timer: 3000,
          });
        });
    },
    delete_user(){
      this.$axios
        .post(
          envs.apiUrl + '/user/delete',
          {
            username: this.username,
            email: this.email,
          },
        )
        .then(re => {
          if (re.data.code == 200) {
            this.$swal({
              toast: true,
              position: 'top-end',
              type: 'success',
              title: '操作成功',
              timer: 1500,
            });
          }
        })
        .catch(err => {
          this.$swal({
            toast: true,
            position: 'top-end',
            type: 'error',
            title: '操作失败，请排查',
            timer: 3000,
          });
        })
      }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .admin {
    .nya-btn{
        margin-bottom: 10px;
    }
    table {
        table-layout: auto;
        width: 100%;
    }
  }
</style>
