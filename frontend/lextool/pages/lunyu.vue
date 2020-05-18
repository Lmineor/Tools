<template>
    <div class="main">
        <nya-container :title="title">
            <!-- <nya-dropdown style="width:33%" label="朝代" :itemlist="itemlist" :nodatatext="nodatatext"></nya-dropdown> -->
            <nya-dropdown v-model="chapter" style="width:33%" :items="chapters" label="章" v-on:change="getparagraphs" />
            <div v-if="hasparagraphs" class="paragraphs">
                <li class="chapter"><span class="prefix">《</span>{{chapter}}<span class="prefix">》</span></li>
                <li v-for="item in paragraphs" :key="item.index" class="paragraph">
                    {{ item }}
                </li>
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
            hasparagraphs: false,
            paragraphs: [],
            chapter: '',
            chapters: [],
            loading : true,
        };
    },
    mounted (){
        this.getchapters()
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
        getparagraphs (id){
            this.chapter = this.chapters[id],
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
    .paragraphs{
        color: #000000;
        .chapter{
            font-size: 35px;
            text-align: center;
            list-style: none;
        }
        .prefix{
            color: #000000;
        }
        .paragraph{
            font-size: 20px;
            margin-top: 10px;
            font-weight: 100;
            text-align: left;
        }
        font-family: "楷体","楷体_GB2312";
    }
}

</style>