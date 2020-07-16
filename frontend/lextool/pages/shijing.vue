<template>
    <div class="main">
        <nya-container :title="title">
          <div>
            <nya-dropdown
                style="width:33%"
                label="诗名"
                :items="shiJingPoems"
                v-on:change="getContent"
                v-on:pagechange="changeTitlePage"
                :total="total"
            />
          </div>
          <div v-if="showContent" class="shijing">
            <li class="title"><span class="prefix">『</span>{{shijingPoem}}<span class="prefix">』</span></li>
            <li class="chapter"><span class="prefix">{{chapter}}·</span>{{section}}</li>
            <li v-for="item in content" :key="item.index" class="content">{{ item }}</li>
          </div>
        </nya-container>

    </div>
</template>

<script>
import envs from '../env'
export default {
    name: 'shijing',
    head() {
        return{
            title:this.title
        }
    },
    data() {
        return {
          title: '诗经',
          defaultPage: 1,
          total: 1,
          shiJingPoems: [],
          shijingPoem:'',
          showContent: false,
          chapter:'',
          section:'',
          content: [],
          loading_content:true
        };
    },
    computed:{
    },
    mounted (){
        this.getShiJingPoems()
    },
    methods: {
        changeTitlePage(current){
            this.$axios
                .get(envs.apiUrl + '/poem/shijing?page=' + current)
                .then(re => {
                    this.shiJingPoems = re.data.poems.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,10);
                    this.total = re.data.total;
                    this.loading = false;
                })
                .catch(err => {
                    this.shiJingPoems = [];
                    this.loading = false;
                });
        },
        getShiJingPoems (){
            this.$store.commit('SET_STORE', {
                key: 'globalLoading',
                value: true
            });
            this.changeTitlePage(this.defaultPage);
            this.$store.commit('SET_STORE', {
              key: 'globalLoading',
              value: false
          });
        },
        getContent(id){
          this.loading_content = true;
          this.shijingPoem = this.shiJingPoems[id]
          this.$axios
            .get(envs.apiUrl + '/poem/shijing?poem=' + this.shijingPoem)
            .then(re => {
                this.content = re.data.content;
                this.chapter = re.data.chapter;
                this.section = re.data.section;
                this.showContent = true;
            })
            .catch(err => {
                this.content = [];
                this.loading = false;
            });
          this.loading_content = false;
        },
    }
};
</script>

<style lang="scss">
.main {
    .shijing{
        font-size: 25px;
        text-align: center;
        list-style: none;
        color: #000000;
        .prefix{
            color: #000000;
        }
        .title{
            margin-top: 20px;
            font-size: 40px;
            font-weight: 100;
        }
        font-family: "楷体","楷体_GB2312";
    }
}

</style>
