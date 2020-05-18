<template>
    <div class="main">
        <nya-container :title="title">
            <!-- <nya-dropdown style="width:33%" label="朝代" :itemlist="itemlist" :nodatatext="nodatatext"></nya-dropdown> -->
            <nya-dropdown
                style="width:33%"
                label="诗名"
                :items="shijingtitles"
                v-on:change="getcontent"
                v-on:pagechange="changeTitlePage"
                :total="total"
            />
            <div v-if="showcontent" class="shijing">
                <li class="title"><span class="prefix">《</span>{{shijingtitle}}<span class="prefix">》</span></li>
                <li class="chapter"><span class="prefix">{{chapter}}·</span>{{section}}</li>
                <li v-for="item in content" :key="item.index" class="content">
                    {{ item }}
                </li>
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
            defaultpage: 1,
            total: 1,
            shijingtitles: [],
            shijingtitle:'',
            showcontent: false,
            chapter:'',
            section:'',
            content: [],
        };
    },
    computed:{
    },
    mounted (){
        this.getshijingtitles()
    },
    methods: {
        changeTitlePage(current){
            this.$axios
                .post(
                    envs.apiUrl + '/poem/shijing',
                    {
                        title:'',
                        page: current,
                    },
                )
                .then(re => {
                    this.shijingtitles = re.data.titles.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'})).slice(0,10);
                    this.total = re.data.total;
                    this.loading = false;
                })
                .catch(err => {
                    this.shijingtitles = [];
                    this.loading = false;
                });
        },
        getshijingtitles (){
            this.changeTitlePage(this.defaultpage);
        },
        getcontent(id){
            this.shijingtitle = this.shijingtitles[id]
            this.$axios
                .post(
                    envs.apiUrl + '/poem/shijing',
                    {
                        title: this.shijingtitle,
                        page: ''
                    },
                )
                .then(re => {
                    this.content = re.data.content;
                    this.chapter = re.data.chapter;
                    this.section = re.data.section;
                    this.showcontent = true;
                })
                .catch(err => {
                    this.content = [];
                    this.loading = false;
                });
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