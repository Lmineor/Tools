<template>
    <div class="main">
        <nya-container :title="title">
          <div class="main-container">
            <div class="left">
              <Card style="width:97%">
                  <p slot="title">
                      <Icon type="logo-freebsd-devil" />
                      诗人
                  </p>
                  <Input
                    search
                    size="small"
                    slot="extra"
                    v-model="keyword"
                    style="width:100px;"
                    @on-search="search_keyword(1)"
                    placeholder="搜索诗人"
                  />
                  <ul v-if="!show_msg" >
                    <Spin v-if="loading_poets" fix>
                        <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                        <div>加载中</div>
                      </Spin>
                      <span v-else v-for="item in poets" :key="item.index">
<!--                        <a href="#">{{item}} </a>-->
                        <Button type="primary" class="author-btn" :title="item" @click="getPoems(item)">{{item}}</Button>
                      </span>
                  </ul>
                  <ul v-else>
                    <span>{{msg}}</span>
                  </ul>
                <Page :total="poet_total" class="page" @on-change='changePoetPage' :page-size="15"/>
              </Card>
              <Card style="width:97%">
                  <p slot="title">
                      <Icon type="logo-freebsd-devil" />
                      诗作
                    <span style="color:blue;">{{poet}}</span>
                  </p>
                  <Input search size="small" slot="extra"  style="width:100px;" placeholder="搜索诗歌"/>
                  <ul >
                      <Spin v-if="loading" fix>
                        <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                        <div>加载中</div>
                      </Spin>
                      <span v-else v-for="item in poems" :key="item.index">
                        <Button type="primary" class="author-btn" :title="item" @click="getContent(item)">{{item}}</Button>
                      </span>
                  </ul>
              </Card>
              <Card style="width:97%">
                  <p slot="title">
                      <Icon type="logo-freebsd-devil" />
                      朝代
                  </p>
                  <ul>
                      <span v-for="item in dynastys" :key="item.index">
                        <Button type="primary" class="author-btn" :title="item">{{item}}</Button>
                      </span>
                  </ul>
              </Card>
            </div>
<!--            <Divider type="vertical" />-->
            <div class="right">
              <Card style="width:100%;">
                  <p slot="title" style="font-size: 20px;color: blue;font-weight: bold;margin-bottom:5px;">
                      {{poem}}
                  </p>
                  <a slot="title" @click="getPoetIntroduction" style="font-size: 15px;">{{dynasty}}：{{poet}}
                  </a>
                  <ul>
                      <Spin v-if="loading_content" fix>
                        <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                        <div>加载中</div>
                      </Spin>
                      <li v-else v-for="item in content" style="list-style: none;">
                          <span class="poem-content">
                            {{item}}
                          </span>
                      </li>
                  </ul>
              </Card>
              <Card v-if="show_introduction" style="width:100%;">
                  <p slot="title">
                      诗人简介
                  </p>
                  <ul>
                    <span class="introduction">
                      {{introduction}}
                    </span>
                  </ul>
              </Card>
            </div>
          </div>
        </nya-container>
    </div>
</template>

<script>
import envs from '../env'
export default {
    name: 'poem',
    head() {
        return{
          title:this.title
        }
    },
    data() {
        return {
          title: '诗歌',
          poem: '春感詩',
          poems: [],
          keyword: '',
          content: ['茫茫南與北，道直事難諧', '榆莢錢生樹，楊花玉糝街',
            '塵縈遊子面，蝶弄美人釵','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋'],
          dynasty:'唐',
          introduction:'是一个很牛逼的诗人',
          poet: '杜甫',
          poets: [],
          page: 1,
          poet_page: 1,
          dynastys: ['唐', '宋'],
          poet_total: 1,
          poem_total: 1,
          msg: '暂无词诗人信息',
          loading: false,
          loading_content:false,
          loading_introduction:false,
          show_introduction:false,
          show_msg: false,
          loading_poets: true,
          is_search: false
        };
    },
    computed:{
    },
    mounted () {
            // this.changeLimit();
            this.getPoets(1);
    },
    methods: {
      changePoetPage(page){
            this.poet_page = page;
            if (!this.is_search){this.getPoets(page)}
            else{this.search_keyword(page)}
        },
      getPoets (page){
        this.show_introduction = false;
        this.dynasty = '唐',
        this.$axios
            .post(
                envs.apiUrl + '/poem/poet/poets',
                {
                    dynasty: '唐',
                    page: page,
                },
            )
            .then(re => {
                this.poets = re.data.poets.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,15);
                this.poet_total = re.data.total;
                this.loading_poets = false;
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
        },
      getPoems(item){
        this.show_introduction = false;
        this.loading = true;
        this.poet = item;
        this.$axios
          .post(
              envs.apiUrl + '/poem/poet/poems',
              {
                  dynasty: '唐',
                  poet: item
              },
          )
          .then(re => {
              this.poems = re.data.poems;
              this.loading = false;
          })
          .catch(err => {
              this.$swal({
                toast: true,
                position: 'top-end',
                type: 'error',
                title: err,
                timer: 3000,
              });
              this.loading = false;
          });
      },
      getContent(item){
        this.poem = item;
        this.loading_content = true;
        this.$axios
          .post(
              envs.apiUrl + '/poem/poet/content',
              {
                  dynasty: '唐',
                  poet: this.poet,
                  poem: this.poem
              },
          )
          .then(re => {
              this.content = re.data.content;
              this.loading_content = false;
          })
          .catch(err => {
              this.$swal({
                toast: true,
                position: 'top-end',
                type: 'error',
                title: err,
                timer: 3000,
              });
              this.loading_content = false;
          });
      },
      getPoetIntroduction(){
        this.loading_info = true;
        this.$axios
          .post(
              envs.apiUrl + '/poem/poet/introduction',
              {
                  dynasty: '唐',
                  poet: this.poet
              },
          )
          .then(re => {
            if(re.data.introduction) {
              this.introduction = re.data.introduction;
            }else{this.introduction = '暂无'}
            this.loading_introduction = false;
            this.show_introduction = true;
          })
          .catch(err => {
              this.$swal({
                toast: true,
                position: 'top-end',
                type: 'error',
                title: err,
                timer: 3000,
              });
              this.loading_introduction = false;
          });
      },
      search_keyword(page){
        if(!this.keyword){
          this.is_search = true;
          this.getPoets(1);
          return;
        }
        this.is_search = true;
        this.$axios
          .post(
              envs.apiUrl + '/poem/poet/search',
              {
                  keyword: this.keyword,
                  page: page,
              },
          )
          .then(re => {
            if(re.data.poets) {
              this.poets = re.data.poets;
              this.show_msg = false;
              this.poet_total = re.data.total;
            }else{this.show_msg = true;}
            this.loading_introduction = false;
            this.show_introduction = true;
          })
          .catch(err => {
              this.$swal({
                toast: true,
                position: 'top-end',
                type: 'error',
                title: err,
                timer: 3000,
              });
              this.loading_introduction = false;
          });
      }
    }
};
</script>

<style lang="scss">
.main {
  .main-container{
    display: table;
    .left{
      width: 45%;
      float:left;
      position: relative;
      .author-btn{
        position: relative;
        margin: 7px;
        width: calc(30% - 7px);
        text-align: center;
        box-sizing: border-box;
        overflow: hidden;
        text-align: center;
        text-overflow: ellipsis;
        white-space: nowrap;
        transition: all 0.3s ease;
        background-color: transparent;
        font-size: 10px;
        color: #1f1f1f;
        border-radius: 4px;
        &:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px 0px rgba(10, 14, 29, 0.04),
                0px 8px 64px 0px rgba(10, 14, 29, 0.08);
        }
      }
      .page{
        width:100%;
        text-align: center;
    }
    }
    .right{

      width: 55%;
      float:left;
      position: relative;
      .poem-content{
        font-family: 楷体;
        font-size: 30px;
      }
      .introduction{
        font-size: 17px;
      }
    }
  }

}

</style>
