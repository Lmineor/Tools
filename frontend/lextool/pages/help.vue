<template>
  <div>
    <nya-container :title=title>
      <div class="help">
        <template v-for="qa in qas">
          <Card class="help-card">
            <p slot="title">
              <Icon type="md-help" />
                {{qa.q}}
            </p>
            <ul>
              <span class="introduction">
                <Icon type="logo-twitch" />
                {{ qa.a }}
              </span>
            </ul>
          </Card>
        </template>
      </div>
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
        {
          'q': '有疑问？',
          'a': '发送邮件给luohai2233@163.com'
        },
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  lang="scss">
  .help {
    display: table;
    width: 100%;
    .help-card {
      margin-bottom: 10px;
      position: relative;
    }
  }
</style>
