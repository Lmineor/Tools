<template>
    <div class="shorturl">
        <nya-container title="短链生成">
            <nya-input
                v-model.trim="url"
                label="请输入URL"
                :placeholder="`${$store.state.env.url}`"
                autocomplete="off"
                autofocus
                fullwidth
                @keyup.enter="getShortUrl"
            />
            <div class="nya-btn" @click="getShortUrl">
                生成
            </div>
        </nya-container>
        <nya-container v-if="res" title="结果">
            <div v-html="res"></div>
        </nya-container>
    </div>
</template>

<script>
import envs from '../env'

export default {
    name: 'ShortUrl',
    head() {
        return{
            title: '短链生成'
        }
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
                this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: '网址不能为空',
                    timer: 1500,
                });
                return false;
            }
            this.$axios
                .post(
                    envs.apiUrl + '/dwz/dwz/',
                    {
                        url: this.url,
                    },
                )
                .then(re => {
                    this.res = re.data.url;
                })
                .catch(err => {
                    this.res = '生成失败';
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
