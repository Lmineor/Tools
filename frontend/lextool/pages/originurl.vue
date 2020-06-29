<template>
    <div class="OriginUrl">
        <nya-container title="短链复原">
            <nya-input
                v-model.trim="dwz"
                label="请输入短链"
                placeholder="0000Ha"
                autocomplete="off"
                autofocus
                fullwidth
                @keyup.enter="getOriginUrl"
            />
            <div class="nya-btn" @click="getOriginUrl">
                还原
            </div>
        </nya-container>
        <nya-container v-if="url" title="结果">
          <div class="res-url"><span>{{url}}</span></div>

<!--            <div v-html="url"></div>-->
        </nya-container>
        <nya-container title="提示" icon="volume-down-outline">
            <ul class="nya-list">
                <li>本站短链可以直接通过访问的方式进行</li>
                <li>格式：www.lex666.online/s/<获得的短链></li>
                <li>例如: <a href = "https://www.lex666.online/s/000007">https://www.lex666.online/s/000002</a>可以跳转到百度</li>
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
            url:'',
            dwz:'',
        };
    },
    methods: {
        checkFormat(){
            pattern = "((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)"
        },
        getOriginUrl() {
            if (this.dwz === ''){
                this.$swal({
                    toast: true,
                    position: 'top-end',
                    type: 'error',
                    title: '内容不能为空',
                    timer: 1500,
                });
                return false;
            }
            this.$axios
                .post(
                    envs.apiUrl + '/dwz/restore',
                    {
                        dwz: this.dwz,
                    },
                )
                .then(re => {
                    this.url = re.data.url;
                })
                .catch(err => {
                    this.url = "生成失败,该短链不存在";
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
    .res-url{
      width: 100%;
      word-break:break-all;
      overflow: hidden;
    }
}
</style>
