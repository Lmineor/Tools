<template>
    <div class="main">
        <nya-container :title="title">
          <div class="main-container">
            <div class="left">
              <Card style="width:97%">
                  <p slot="title">
                      章节
                  </p>
                  <ul>
                      <span v-for="item in chapters" :key="item.index">
                        <Button type="primary" class="author-btn" :title="item" @click="getparagraphs(item)">{{item}}</Button>
                      </span>
                  </ul>
              </Card>
            </div>
            <div class="right">
              <Card >
                  <p slot="title" style="font-size: 20px;color: blue;font-weight: bold;margin-bottom:5px;">
                      {{chapter}}
                  </p>
                  <ul>
                      <Spin v-if="loading_paragraphs" fix>
                        <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                        <div>加载中</div>
                      </Spin>
                      <li v-else v-for="item in paragraphs" style="list-style: none;">
                          <span class="poem-content">
                            {{item}}
                            <Divider size="small" />
                          </span>
                      </li>
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
    name: 'lunyu',
    head() {
        return{
            title:this.title
        }
    },
    data() {
        return {
            title: '论语',
            loading_paragraphs: false,
            paragraphs: [],
            chapter: '八佾第三',
            chapters: [],
            loading : true,
        };
    },
    mounted (){
        this.getchapters();
        this.getparagraphs (this.chapter)
    },
    methods: {
        getchapters(){
            this.loading = true,
            this.$axios
                .get(
                    envs.apiUrl + '/poem/lunyu',
                )
                .then(re => {
                    this.chapters = re.data.chapters.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));;
                    this.loading = false;
                })
                .catch(err => {
                    this.chapters = [];
                    this.loading = false;
                });
        },
        getparagraphs (chapter){
            this.chapter = chapter,
            this.loading = true,
            this.hasparagraphs = false,
            this.$axios
                .post(
                    envs.apiUrl + '/poem/lunyu',
                    {
                        chapter: this.chapter,
                    },
                )
                .then(re => {
                    this.paragraphs = re.data.paragraphs;
                    this.hasparagraphs = true
                    this.loading = false;
                })
                .catch(err => {
                    this.paragraphs = [];
                    this.loading = false;
                });
        },
    }
};
</script>

<style lang="scss">
.main {
  .main-container{
    display: table;
    .left{
      width: 33%;
      float:left;
      position: relative;
      .author-btn{
        position: relative;
        margin: 7px;
        width: calc(40% - 5px);
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
      overflow:scroll;
      height: 556px;
      width: 65%;
      float:right;
      position: relative;
      .poem-content{
        font-family: 楷体;
        font-size: 20px;
        font-weight: bold;
      }
      .introduction{
        font-size: 17px;
      }
    }
  }

}


</style>
