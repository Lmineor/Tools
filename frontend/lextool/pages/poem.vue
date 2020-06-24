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
                v-on:change="getPoets"
            />
            <nya-dropdown
                v-if="showPoets"
                v-model="poet"
                style="width:33%"
                :items="poets"
                label="诗人"
                :total="total"
                v-on:change="getPoems"
                v-on:pagechange="changeAuthorPage"
            />
            <nya-dropdown
                v-if="showPoems"
                v-model="poem"
                style="width:33%"
                :items="poems"
                label="诗名"
                :pageable=false
                v-on:change="getContent"
            />
            <div v-if="hasPoem" class="poem">
                <li class="poem title"><span class="prefix">『</span>{{poem}}<span class="prefix">』</span></li>
                <li class="poem poet"><span class="prefix">{{dynasty}}·</span>{{poet}}</li>
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
            showPoets: false,
            showPoems: false,
            getDynasty: false,
            hasPoem: false,
            dynastys:['唐','宋'],
            poets: [],
            poems: [],
            poem: '',
            dynasty:'',
            poet:'',
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
                    envs.apiUrl + '/poem/poet/poets',
                    {
                        dynasty: this.dynasty,
                        page: current,
                    },
                )
                .then(re => {
                    this.poets = re.data.poets.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,15);
                    this.showPoets = true;
                    this.loading = false;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getPoets (id){
            this.dynasty = this.dynastys[id],
            this.loading = true,
            this.poets = [],
            this.poems = [],
            this.poem = '',
            this.poet = '',
            this.showPoets = false,
            this.showPoems = false,
            this.hasPoem = false,
            this.$axios
                .post(
                    envs.apiUrl + '/poem/poet/poets',
                    {
                        dynasty: this.dynastys[id],
                        page: this.defaultpage,
                    },
                )
                .then(re => {
                    this.poets = re.data.poets.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,15);
                    this.total = re.data.total;
                    this.showPoets = true;
                    this.loading = false;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getPoems (id){
            this.poet = this.poets[id],
            this.poems = [],
            this.poem = '',
            this.hasPoem = false,
            this.showPoems = false,
            this.$axios
                .post(
                    envs.apiUrl + '/poem/poet/poems',
                    {
                        dynasty: this.dynasty,
                        poet: this.poet
                    },
                )
                .then(re => {
                    this.poems = re.data.poems.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));
                    this.showPoems = true
                    this.loading = true;
                })
                .catch(err => {
                    this.res = '生成失败';
                    this.loading = false;
                });
        },
        getContent(id){
            this.poem = this.poems[id]
            this.$axios
                .post(
                    envs.apiUrl + '/poem/poet/content',
                    {
                        dynasty: this.dynasty,
                        poet: this.poet,
                        poem: this.poem
                    },
                )
                .then(re => {
                    this.content = re.data.content;
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
