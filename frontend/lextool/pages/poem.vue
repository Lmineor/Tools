<template>
    <div class="poem">开发中
    </div>
</template>

<script>
import envs from '../env'
export default {
    name: 'ShortUrl',
    head() {
        return this.$store.state.currentTool.head;
    },
    data() {
        return {
            res:'',
            url:'',
        };
    },
    methods: {
        checkFormat(){
            pattern = "((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)"
        },
        getShortUrl() {
            if (this.url === ''){
                window.alert("网址不能为空");
                return false;
            }
            this.$axios
                .post(
                    envs.apiUrl + '/shorturl',
                    {
                        url: this.url,
                    },
                )
                .then(re => {
                    this.res = re.data.url;
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
.shorturl {
    .nya-btn {
        margin-top: 15px;
    }
}
</style>