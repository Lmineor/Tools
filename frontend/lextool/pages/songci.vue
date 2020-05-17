<template>
    <div class="main">
        <nya-container :title="title">
            <nya-dropdown
                v-model="author"
                style="width:33%"
                label="词人"
                :items="authors"
                v-on:change="getrhythmics"
                v-on:pagechange="changeAuthorPage"
                :total="total"
            />
            <nya-dropdown
                v-if="showRhythmics"
                v-model="rhythmic"
                style="width:33%"
                :items="rhythmics"
                :pageable="false"
                label="词牌名"
                v-on:change="getparagraphs"
            />
            <div v-if="hasparagraphs" class="content">
                <li class="title"><span class="prefix">《</span>{{rhythmic}}<span class="prefix">》</span></li>
                <li class="writer"><span class="prefix">宋·</span>{{author}}</li>
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
            title: '宋词',
            hasparagraphs: false,
            paragraphs: [],
            author: '',
            authors: [],
            rhythmics: [],
            rhythmic: '',
            loading : true,
            showAuthors: false,
            showRhythmics: false,
            defaultpage:1,
            total: 1,
        };
    },
    mounted (){
        this.getauthors()
    },
    methods: {
        changeAuthorPage(current){
            this.$axios
                .post(
                    envs.apiUrl + '/poem/songci',
                    {
                        author: '',
                        rhythmic: '',
                        page: current,
                    },
                )
                .then(re => {
                    this.authors = re.data.authors.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));
                    this.loading = false;
                })
                .catch(err => {
                    this.authors = [];
                    this.loading = false;
                });
        },
        getauthors(){
            this.showAuthors = true,
            this.author = '',
            this.loading = true,
            this.$axios
                .post(
                    envs.apiUrl + '/poem/songci',
                    {
                        author: '',
                        rhythmic: '',
                        page: this.defaultpage,
                    },
                )
                .then(re => {
                    this.authors = re.data.authors.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));
                    this.total = re.data.total;
                    this.loading = false;
                })
                .catch(err => {
                    this.authors = [];
                    this.loading = false;
                });
        },
        getrhythmics (id){
            this.author = this.authors[id],
            this.showRhythmics = false,
            this.loading = true,
            this.hasparagraphs = false,
            this.rhythmics = [],
            this.rhythmic = '',
            this.$axios
                .post(
                    envs.apiUrl + '/poem/songci',
                    {
                        author: this.authors[id],
                        rhythmic: '',
                        page: '',
                    },
                )
                .then(re => {
                    this.rhythmics = re.data.rhythmics.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));
                    this.loading = false;
                    this.showRhythmics = true;
                })
                .catch(err => {
                    this.rhythmics = [];
                    this.loading = false;
                });
        },
        getparagraphs (id){
            this.loading = true,
            this.hasparagraphs = false,
            this.rhythmic = this.rhythmics[id],
            this.$axios
                .post(
                    envs.apiUrl + '/poem/songci',
                    {
                        author: this.author,
                        rhythmic: this.rhythmics[id],
                        page: '',
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
        .content{
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