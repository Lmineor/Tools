<template>
    <div class="sci">
        <nya-container title="Sci-Hub 可用网址">
          <table class="nya-table">
              <tr>
                  <th>网址</th>
                  <th>连接测试</th>
              </tr>
              <tr v-for="(item, index) in links" :key="index">
                  <td><a :href="item.url" target="_blank" rel="noopener noreferrer" class='links'>{{ item.url }}</a></td>
                  <td>
                    <Spin v-if="!item.status" style="float: left">
                        <Icon type="ios-loading" size=20 class="spin-icon-load"></Icon>
                    </Spin>
                    <span v-else>{{ item.status }}</span>
                  </td>
              </tr>
          </table>
<!--            <div v-for="(item, index) in links" :key="index">-->
<!--                 <a :href="item" target="_blank" rel="noopener noreferrer" class='links'>{{ item }}</a>-->
<!--            </div>-->
        </nya-container>
        <nya-container title="公告" icon="volume-down-outline">
            <ul class="nya-list">
                <li>数据来源 <a href="https://www.howsci.com/sci-hub-alternative.html" target="_blank" rel="noopener noreferrer">Sci-Hub 可用网址 | 科研动力</a></li>
                <li>仅供学习科研使用噢</li>
                <li>有新的可用链接<a href="/comment_board">欢迎反馈</a></li>
            </ul>
        </nya-container>
    </div>
</template>

<script>
import envs from "../env";

export default {
    name: 'sci',
    head() {
        return {
            title: 'sci-hub可用网址'
        };
    },
    data() {
        return {
          links: [
            {'url': 'https://www.sci-hub.shop/', 'status': ''},
            // {'url': 'http://www.sci-hub.bz/', 'status': ''},
            // {'url': 'http://sci-hub.hk/', 'status': ''},
            {'url': 'http://sci-hub.tw/', 'status': ''},
          ],
        };
    },
  mounted() {
      this.testUrl()
  },
  methods:{
    testUrl(){
      for (let i = 0; i < this.links.length; i++) {
          this.$axios
            .post(envs.apiUrl + '/sci/test',
            {
                url: this.links[i].url
            },
            )
            .then(re => {
              console.log(re)
              if(re.data.times < 0) {
                this.links[i].status = '不可用';
              }else{
                this.links[i].status = re.data.times + '毫秒';
              }
                // this.links[i].status = re.response.status;
              })
            .catch(err => {
                this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: err,
                    timer: 3000,
                  });
            });
       }
      }
  },
};
</script>

<style lang="scss">
.sci {
    table {
        table-layout: auto;
        width: 100%;
    }
    .spin-icon-load{
        animation: ani-demo-spin 1s linear infinite;
    }
    @keyframes ani-demo-spin {
          from { transform: rotate(0deg);}
          50%  { transform: rotate(180deg);}
          to   { transform: rotate(360deg);}
    }
}

</style>
