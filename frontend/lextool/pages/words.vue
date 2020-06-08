<template>
    <div class="words">
        <nya-container :title="title">
            <Table stripe :columns="columns" :data="words"></Table>
        </nya-container>
    </div>
</template>

<script>
import envs from '../env'

export default {
    name: 'ShortUrl',
    head() {
        return{
            title: this.title
        }
    },
    data() {
        return {
            title: '每日英语',
            columns: [
                    {
                        title: '单词',
                        key: 'word'
                    },
                    {
                        title: '词义',
                        key: 'translation'
                    }
                ],
            words: [],
        };
    },
    mounted (){
        this.getWords()
    },
    methods: {
        getWords() {
            this.$axios
                .get(envs.apiUrl + '/words/daily',)
                .then(re => {
                    this.words = re.data.words;
                })
                .catch(err => {
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        type: 'error',
                        title: 'error' + err,
                        timer: 3000,
                    });
                });
        },
    }
};
</script>

<style lang="scss">
.shorturl {
    .nya-btn {
        margin-top: 15px;
    }
}
</style>