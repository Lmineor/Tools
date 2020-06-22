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
                  <Input search size="small" slot="extra"  style="width:100px;" placeholder="搜索诗人"/>
                  <ul>
                      <span v-for="item in authors" :key="item.index">
<!--                        <a href="#">{{item}} </a>-->
                        <Button type="primary" class="author-btn" :title="item">{{item}}</Button>
                      </span>
                  </ul>
              </Card>
              <Card style="width:97%">
                  <p slot="title">
                      <Icon type="logo-freebsd-devil" />
                      诗歌
                  </p>
                  <Input search size="small" slot="extra"  style="width:100px;" placeholder="搜索诗歌"/>
                  <ul>
                      <span v-for="item in authors" :key="item.index">
                        <Button type="primary" class="author-btn" :title="item">{{item}}</Button>
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
                  <a slot="title" href="#" style="font-size: 15px;">{{dynasty}}：{{author}}
                  </a>
                  <ul>
                      <li v-for="item in content">
                          <span class="poem-content">
                            {{item}}
                          </span>
                      </li>
                  </ul>
              </Card>
              <Card style="width:100%;">
                  <p slot="title">
                      诗人简介
                  </p>
                  <ul>
                    <span>
                      {{desc}}
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
          content: ['茫茫南與北，道直事難諧', '榆莢錢生樹，楊花玉糝街',
            '塵縈遊子面，蝶弄美人釵','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋','却憶青山上，雲門掩竹齋'],
          dynasty:'唐',
          author: '杜甫',
          desc:'是一个很牛逼的诗人',
          movieList: [
                    {
                        name: 'The Shawshank Redemption',
                        url: 'https://movie.douban.com/subject/1292052/',
                        rate: 9.6
                    },
                    {
                        name: 'Leon:The Professional',
                        url: 'https://movie.douban.com/subject/1295644/',
                        rate: 9.4
                    },
                    {
                        name: 'Farewell to My Concubine',
                        url: 'https://movie.douban.com/subject/1291546/',
                        rate: 9.5
                    },
                    {
                        name: 'Forrest Gump',
                        url: 'https://movie.douban.com/subject/1292720/',
                        rate: 9.4
                    },
                    {
                        name: 'Life Is Beautiful',
                        url: 'https://movie.douban.com/subject/1292063/',
                        rate: 9.5
                    },
                    {
                        name: 'Spirited Away',
                        url: 'https://movie.douban.com/subject/1291561/',
                        rate: 9.2
                    },
                    {
                        name: 'Schindlers List',
                        url: 'https://movie.douban.com/subject/1295124/',
                        rate: 9.4
                    },
                    {
                        name: 'The Legend of 1900',
                        url: 'https://movie.douban.com/subject/1292001/',
                        rate: 9.2
                    },
                    {
                        name: 'WALL·E',
                        url: 'https://movie.douban.com/subject/2131459/',
                        rate: 9.3
                    },
                    {
                        name: 'Inception',
                        url: 'https://movie.douban.com/subject/3541415/',
                        rate: 9.2
                    }
                ],
          randomMovieList: [],
          authors: [],
          defaultpage: 1,
          dynastys: ['唐', '宋']
        };
    },
    computed:{
    },
    mounted () {
            this.changeLimit();
            this.getwriters();
    },
    methods: {
       getwriters (){
            this.dynasty = '唐',
            this.loading = true,
            this.writers = [],
            this.poem = '',
            this.$axios
                .post(
                    envs.apiUrl + '/poem/getauthor',
                    {
                        dynasty: '唐',
                        page: this.defaultpage,
                    },
                )
                .then(re => {
                    this.authors = re.data.authors.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,10);
                    this.total = re.data.total;
                    this.showWriters = true;
                    this.loading = false;
                    this.poem = '从军行';
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
      changeLimit () {
                function getArrayItems(arr, num) {
                    const temp_array = [];
                    for (let index in arr) {
                        temp_array.push(arr[index]);
                    }
                    const return_array = [];
                    for (let i = 0; i<num; i++) {
                        if (temp_array.length>0) {
                            const arrIndex = Math.floor(Math.random()*temp_array.length);
                            return_array[i] = temp_array[arrIndex];
                            temp_array.splice(arrIndex, 1);
                        } else {
                            break;
                        }
                    }
                    return return_array;
                }
                this.randomMovieList = getArrayItems(this.movieList, 5);
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
    }
    .right{
      width: 55%;
      float:left;
      position: relative;
      .poem-content{
        font-family: 楷体;
        font-size: 30px;
      }
    }
  }

}

</style>
