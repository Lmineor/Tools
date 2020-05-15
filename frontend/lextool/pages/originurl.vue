<template>
    <div class="OriginUrl">
        <nya-container title="短链复原">
            <nya-input
                v-model.trim="shorturl"
                label="请输入短链"
                placeholder="0000Ha"
                autocomplete="off"
                autofocus
                fullwidth
            />
            <div class="nya-btn" @click="getOriginUrl">
                还原
            </div>
        </nya-container>
        <nya-container v-if="OriginUrl" title="结果">
            <div v-html="OriginUrl"></div>
        </nya-container>
        <nya-container title="提示" icon="volume-down-outline">
            <ul class="nya-list">
                <li>本站短链可以直接通过访问的方式进行</li>
                <li>格式：www.lex666.online/s/<获得的短链></li>
                <li>例如: <a href = "https://www.lex666.online/s/000002">https://www.lex666.online/s/000002</a></li>
            </ul>
        </nya-container>

    </div>
</template>

<script>
import envs from '../env'
export default {
    name: 'OriginUrl',
    head() {
        return {
            title: '短链还原'
        };
    },
    data() {
        return {
            OriginUrl:'',
            shorturl:'',
        };
    },
    methods: {
        checkFormat(){
            pattern = "((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)"
        },
        getOriginUrl() {
            if (this.shorturl === ''){
                window.alert("输入内容不能为空");
                return false;
            }
            this.$axios
                .post(
                    envs.apiUrl + '/shorturl/OriginUrl',
                    {
                        shorturl: this.shorturl,
                    },
                )
                .then(re => {
                    this.OriginUrl = re.data.OriginUrl;
                })
                .catch(err => {
                    this.OriginUrl = '生成失败,该短链不存在';
                    this.loading = false;
                });
        },
    }
};
</script>

<style lang="scss">
.OriginUrl {
    .nya-btn {
        margin-top: 15px;
    }
}
</style>