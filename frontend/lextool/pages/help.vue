<template>
  <div class="help">
    <nya-container :title=title>
      <template v-for="qa in qas">
        <li style="font-size:25px; list-style: none;">Q: {{ qa.q }}</li>
        <li style="font-size:17px; list-style: none;">A：{{ qa.a }}</li>
        <li style="font-size:17px; list-style: none;"><br></li>
      </template>
    </nya-container>

  </div>
</template>

<script>
import envs from '../env'



export default {
  name: 'help',
  data () {
    return {
      title: '帮助中心',
      qas: [
        {
          'q': '忘记密码怎么办', 
          'a': '用你注册时的邮箱，发送邮件给luohai2233@163.com,格式：邮件主题：忘记密码+你注册时的邮箱，正文： 同主题'
        },
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
</style>
