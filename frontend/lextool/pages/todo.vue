<template>
  <div class="todo">
    <nya-container :title=title class="todos">
      <div v-for="(todo, index) in todos" track-by="$index">
          <Card class="todo-card">
            <p slot="title">
              <Icon type="md-help" />
                {{todo.ddl}}
            </p>
            <Radio v-model="todo.finished" slot="extra" @on-change="finish(index)">完成</Radio>
            <ul>
              <span class="content">
                <Icon type="logo-twitch" />
                {{ todo.todo }}
              </span>
            </ul>
          </Card>
        </div>
    </nya-container>
    <nya-container :title=title2 class="todos">
      <template v-for="(todo, index) in finished_todos">
          <Card class="todo-card">
            <p slot="title">
              <Icon type="md-help" />
                {{todo.ddl}}
            </p>
            <Radio v-model="todo.cancel" slot="extra" @on-change="cancel(index)">撤销</Radio>
            <ul>
              <span class="content">
                <Icon type="logo-twitch" />
                {{ todo.todo }}
              </span>
            </ul>
          </Card>
        </template>
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
      rows: 23,
      finished: false,
      todos: [
                {'ddl':'今天','todo':'完成开发1', 'finished': false, 'cancel': true, 'id': 'xxxxxxx'},
                {'ddl':'今天','todo':'完成开发2', 'finished': false, 'cancel': true, 'id': 'xxxxxxx'},
                {'ddl':'今天','todo':'完成开发3', 'finished': false, 'cancel': true, 'id': 'xxxxxxx'},
                {'ddl':'今天','todo':'完成开发4', 'finished': false, 'cancel': true, 'id': 'xxxxxxx'},
            ],
      finished_todos: [
                {'ddl':'今天','todo':'完成1', 'finished': true, 'cancel': false, 'id': 'xxxxxxx'},
                {'ddl':'今天','todo':'完成2', 'finished': true, 'cancel': false, 'id': 'xxxxxxx'},
                {'ddl':'今天','todo':'完成3', 'finished': true, 'cancel': false, 'id': 'xxxxxxx'},
                {'ddl':'今天','todo':'完成4', 'finished': true, 'cancel': false, 'id': 'xxxxxxx'},
            ],
      title: 'ToDo',
      title2: '已完成',
      email: '',
      password: '',
      isFocus: false,
      loading: true,
      user: ''
    }
  },
  mounted (){
    this.$axios.defaults.auth = {
        username: Cookie.get('auth'),
        password: ''
    },
    this.loading = false;
  },
  methods: {
    load_todo(){
      this.$axios
        .get(envs.apiUrl + '/todo/todos')
        .then(re => {
            this.todos = re.data.todos;
        })
        .catch(err => {
            this.$Message.error(err);
        });
    },
    load_finish(){
      this.$axios
        .get(envs.apiUrl + '/todo/load_finish')
        .then(re => {
            this.finished_todos = re.data.finished_todos;
        })
        .catch(err => {
            this.$Message.error(err);
        });
    },
    finish(index) {
      this.$axios
        .post(envs.apiUrl + '/todo/finish',{"id": this.todos[index].id})
        .then(re => {
            this.load_todo();
            this.load_finish()
        })
        .catch(err => {
            this.$Message.error(err);
        });
      this.$Message.info("Good Job!");
    },
    cancel(index) {
     this.$axios
        .post(envs.apiUrl + '/todo/cancel',{"id": this.todos[index].id})
        .then(re => {
            this.load_todo();
            this.load_finish()
        })
        .catch(err => {
            this.$Message.error(err);
        });
      this.$Message.info("Good Job!");
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .todo {
    .todos {
      display: table;
      width: 100%;
      .todo-card {
        width: 30%;
        float: left;
        margin-left: 2%;
        margin-top: 2%;
      }
    }
  }
</style>
