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

export default {
    name: 'ShortUrl',
    head() {
        return this.$store.state.currentTool.head;
    },
    data() {
        return {
            res:'',
        };
    },
    methods: {
        getShortUrl() {
            this.$axios
                .post(
                    'http://localhost:5000/shorten',
                    {
                        url: this.url,
                    },
                )
                .then(re => {
                    console.log(re);
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