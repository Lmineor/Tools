<template>
    <div class="main">
        <nya-container :title="title">
            <nya-dropdown
                v-model="poet"
                style="width:33%"
                label="词人"
                :items="poets"
                v-on:change="getRhythmics"
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
                v-on:change="getParagraphs"
            />
            <div v-if="hasparagraphs" class="content">
                <li class="title"><span class="prefix">『</span>{{rhythmic}}<span class="prefix">』</span></li>
                <li class="writer"><span class="prefix">宋·</span>{{poet}}</li>
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
            poet: '',
            poets: [],
            rhythmics: [],
            rhythmic: '',
            loading : true,
            showPoets: false,
            showRhythmics: false,
            defaultpage:1,
            total: 1,
        };
    },
    mounted (){
        this.getAuthors()
    },
    methods: {
        changeAuthorPage(current){
            this.$axios
                .get(envs.apiUrl + '/poem/songci?page=' + current)
                .then(re => {
                    this.poets = re.data.poets.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));
                    this.loading = false;
                })
                .catch(err => {
                    this.authors = [];
                    this.loading = false;
                });
        },
        getAuthors(){
            this.showPoets = true,
            this.poet = '',
            this.loading = true,
            this.$axios
                .get(envs.apiUrl + '/poem/songci?page=' + this.defaultpage)
                .then(re => {
                    this.poets = re.data.poets.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', {sensitivity: 'accent'}));
                    this.total = re.data.total;
                    this.loading = false;
                })
                .catch(err => {
                    this.poets = [];
                    this.loading = false;
                });
        },
        getRhythmics (id){
            this.poet = this.poets[id],
            this.showRhythmics = false,
            this.loading = true,
            this.hasparagraphs = false,
            this.rhythmics = [],
            this.rhythmic = '',
            this.$axios
                .get(envs.apiUrl + '/poem/songci?poet=' + this.poets[id])
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
        getParagraphs (id){
            this.loading = true,
            this.hasparagraphs = false,
            this.rhythmic = this.rhythmics[id],
            this.$axios
                .get(
                    envs.apiUrl + '/poem/songci?poet=' + this.poet + '&rhythmic=' + this.rhythmics[id])
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
