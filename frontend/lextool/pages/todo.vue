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
import {validUsername} from '@/utils/validate'


export default {
  // middleware: 'authenticated', // 需要登录
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

    // this.getmemo();
    // // setInterval(() => {
    // //     this.savememo();//保存表单信息的操作
    // //   },20000)
    this.loading = false;
  },
  methods: {
    finish(index) {
      //
      let item = this.todos.splice(index, 1);
      console.log(item);
      item.cancel = false;
      // item.finished = true;
      this.$forceUpdate();
      this.finished_todos.push(item);

    },
    cancel(index) {
      let item = this.finished_todos[index];
      item.finished = false;
      item.cancel = true;
      this.todos.push(item);
      this.finished_todos.splice(index, 1);
      console.log(index);
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
