<template>
    <div class="main">
        <nya-container :title="title">
            <nya-dropdown
                v-if="showDynasty"
                v-model="dynasty"
                style="width:33%" 
                :items="dynastys" 
                label="朝代" 
                :pageable="false" 
                v-on:change="getwriters" 
            />
            <nya-dropdown
                v-if="showWriters"
                v-model="writer"
                style="width:33%"
                :items="writers"
                label="诗人"
                :total="total"
                v-on:change="getpoems"
                v-on:pagechange="changeAuthorPage"
            />
            <nya-dropdown
                v-if="showPoems"
                v-model="poem"
                style="width:33%"
                :items="poems"
                label="诗名"
                :pageable=false
                v-on:change="getcontent"
            />
            <div v-if="hasPoem" class="poem">
                <li class="poem title"><span class="prefix">《</span>{{poem}}<span class="prefix">》</span></li>
                <li class="poem writer"><span class="prefix">{{dynasty}}·</span>{{writer}}</li>
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
        return{
            title:this.title
        }
    },
    data() {
        return {
            title: '诗歌',
            showDynasty: true,
            showWriters: false,
            showPoems: false,
            getDynasty: false,
            hasPoem: false,
            dynastys:['唐','宋'],
            writers: [],
            poems: [],
            poem: '',
            dynasty:'',
            writer:'',
            content: [''],
            loading : false,
            defaultpage: 1,
            total: ''
        };
    },
    computed:{
    },
    methods: {
        changeAuthorPage(current){
            this.$axios
                .post(
                    envs.apiUrl + '/poem/getauthor',
                    {
                        dynasty: this.dynasty,
                        page: current,
                    },
                )
                .then(re => {
                    this.writers = re.data.authors.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,10);
                    this.showWriters = true;
                    this.loading = false;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getwriters (id){
            this.dynasty = this.dynastys[id],
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
                        dynasty: this.dynastys[id],
                        page: this.defaultpage,
                    },
                )
                .then(re => {
                    this.writers = re.data.authors.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,10);
                    this.total = re.data.total;
                    this.showWriters = true;
                    this.loading = false;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getpoems (id){
            this.writer = this.writers[id],
            this.poems = [],
            this.poem = '',
            this.hasPoem = false,
            this.showPoems = false,
            this.$axios
                .post(
                    envs.apiUrl + '/poem/gettitle',
                    {
                        dynasty: this.dynasty,
                        author: this.writer
                    },
                )
                .then(re => {
                    this.poems = re.data.titles.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));
                    this.showPoems = true
                    this.loading = true;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getcontent(id){
            this.poem = this.poems[id]
            this.$axios
                .post(
                    envs.apiUrl + '/poem/getpoem',
                    {
                        dynasty: this.dynasty,
                        author: this.writer,
                        title: this.poem
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