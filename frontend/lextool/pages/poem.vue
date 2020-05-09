<template>
    <div class="main">
        <nya-container title="诗词歌赋">
            <!-- <nya-dropdown style="width:33%" label="朝代" :itemlist="itemlist" :nodatatext="nodatatext"></nya-dropdown> -->
            <nya-select v-if="showDynasty" v-model="dynasty" style="width:33%" :items="dynastys" label="朝代" v-on:change="getwriters" />
            <nya-select  v-if="showWriters" v-model="writer" style="width:33%" :items="writers" label="诗人"  v-on:change="getpoems"/>
            <nya-select  v-if="showPoems" v-model="poem" style="width:33%" :items="poems" label="诗（词）名" v-on:change="getcontent"/>
            <div v-if="hasPoem" class="poem">
                <li class="poem title"><span class="prefix">《</span>{{poems[poem]}}<span class="prefix">》</span></li>
                <li class="poem writer"><span class="prefix">{{dynastys[dynasty]}}·</span>{{writers[writer]}}</li>
                <li v-for="item in content" :key="item.index" class="poem content">
                    {{ item }}
                </li>
            </div>
        </nya-container>
        
    </div>
</template>

<script>
import envs from '../env'
export default {
    name: 'poem',
    head() {
        return this.$store.state.currentTool.head;
    },
    data() {
        return {
            showDynasty: true,
            showWriters: false,
            showPoems: false,
            getDynasty: false,
            hasPoem: false,
            dynastys:[
                    '唐',
                    '宋',
                    '元',
            ],
            writers: [],
            poems: [],
            poem: '',
            dynasty:'',
            writer:'',
            content: [''],
            loading : false,
        };
    },
    computed:{
    },
    methods: {
        dropDownClick(e) {
        console.log(e.name, e.val)
        },
        getwriters (){
            this.loading = true,
            this.writers = [],
            this.poems = [],
            this.poem = '',
            this.writer = '',
            this.showWriters = false,
            this.showPoems = false,
            this.hasPoem = false,
            this.$axios
                .post(
                    envs.apiUrl + '/poem/getauthor',
                    {
                        dynasty: this.dynastys[this.dynasty],
                    },
                )
                .then(re => {
                    this.writers = re.data.authors;
                    this.showWriters = true
                    this.loading = false;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getpoems (){
            this.poems = [],
            this.poem = '',
            this.hasPoem = false,
            this.showPoems = false,
            this.$axios
                .post(
                    envs.apiUrl + '/poem/gettitle',
                    {
                        dynasty: this.dynastys[this.dynasty],
                        author: this.writers[this.writer]
                    },
                )
                .then(re => {
                    this.poems = re.data.titles;
                    this.showPoems = true
                    this.loading = true;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getcontent(){
            this.$axios
                .post(
                    envs.apiUrl + '/poem/getpoem',
                    {
                        dynasty: this.dynastys[this.dynasty],
                        author: this.writers[this.writer],
                        title: this.poems[this.poem]
                    },
                )
                .then(re => {
                    this.content = re.data.poem.split('。'),
                    this.hasPoem = true
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
    }
};
</script>

<style lang="scss">
.main {
    .poem{
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