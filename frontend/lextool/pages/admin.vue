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
                  <td>{{item.wordsbook}}</td>
                  <td>
                    <Button type="primary" @click="update(index, 'chgpsw')">初始化密码</Button>
                  </td>
                  <td>
                    <Button type="warning" @click="update(index, 'deluser')">删除用户</Button>
                  </td>
              </tr>
          </table>
      </div>
    </nya-container>

    <nya-container :title=title2>
        <div>
            <table class="nya-table">
                <tr>
                    <th style="width: 80px;">id</th>
                    <th>内容</th>
                    <th style="width: 200px;">邮箱</th>
                    <th style="width: 150px;">类型</th>
                    <th style="width: 150px;">反馈时间</th>
                    <th style="width: 100px;">通过审核</th>
                    <th style="width: 100px;">已解决</th>
                </tr>
                <tr v-for="(item, index) in comments" :key="index">
                  <td>{{ item.id }}</td>
                  <td style="overflow: scroll">
                    <p>{{ item.content }}</p>
                  </td>
                  <td>{{item.email}}</td>
                  <td>{{item.comment_type}}</td>
                  <td>{{item.create_at}}</td>
                    <td>
                      <Button type="primary" @click="reviewed(index)">Ok</Button>
                    </td>
                    <td>
                      <Button type="warning" @click="solved(index)">解决</Button>
                    </td>
                </tr>
            </table>
        </div>
    </nya-container>
  </div>

</template>

<script>

const Cookie = process.client ? require("js-cookie") : undefined;
import envs from '../env'


export default {
  middleware: 'authenticated', // 需要登录
  name: 'admin',
  data () {
    return {
      title: '用户管理',
      title2: '留言管理',
      username: '',
      email: '',
      password: '',
      users: Array,
      comments: Array
    }
  },
  mounted (){
    this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      },
    this.getUsers();
    this.load_comments_to_review()
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
          envs.apiUrl + '/admin/users',
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
    update(index, action){
      this.$axios
        .post(
          envs.apiUrl + '/admin/updates',
          {
            action:action,
            email: this.users[index].email,
            password: '123456abc',
            wordsbook:'CET4'
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
      this.getUsers();
    },
    load_comments_to_review(){
      this.$axios.defaults.auth = {
          username: Cookie.get('auth'),
          password: ''
      };
      this.$axios
        .get(envs.apiUrl + '/admin/load_comment')
        .then(re => {
          if (re.data.data) {
            this.comments = re.data.data;
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
      },
    reviewed(index){
      this.$axios
        .post(envs.apiUrl + '/admin/review_comment',{"id": this.comments[index].id,"key":"review"})
        .then(re => {
          if (re.data.code===200) {
            this.$Message.info('操作成功');
          }else{
            this.$Message.error('操作失败');
          }
        })
        .catch(err => {
          this.$Message.error('操作失败，请排查');
        })
      },
    solved(index){
      this.$axios
        .post(envs.apiUrl + '/admin/review_comment',{"id": this.comments[index].id, "key":"solve"})
        .then(re => {
          if (re.data.code===200) {
            this.$Message.info('操作成功');
          }else{
            this.$Message.error('操作失败');
          }
        })
        .catch(err => {
          this.$Message.error('操作失败，请排查');
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
        table-layout: fixed;
        width: 100%;
    }
  }
</style>
