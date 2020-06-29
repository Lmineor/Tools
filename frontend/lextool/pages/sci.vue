<template>
    <div class="sci">
        <nya-container title="Sci-Hub 可用网址">
            <div v-for="(item, index) in links" :key="index">
                 <a :href="item" target="_blank" rel="noopener noreferrer" class='links'>{{ item }}</a>
            </div>
        </nya-container>
        <nya-container title="公告" icon="volume-down-outline">
            <ul class="nya-list">
                <li>数据来源 <a href="https://www.howsci.com/sci-hub-alternative.html" target="_blank" rel="noopener noreferrer">Sci-Hub 可用网址 | 科研动力</a></li>
                <li>仅供学习科研使用噢</li>
                <li>有新的可用链接<a href="/comment_board">欢迎反馈</a></li>
            </ul>
        </nya-container>
    </div>
</template>

<script>
export default {
    name: 'sci',
    head() {
        return {
            title: 'sci-hub可用网址'
        };
    },
    data() {
        return {
            links: [
                'https://www.sci-hub.shop/',
                'http://www.sci-hub.bz/',
                'http://sci-hub.hk/',
                'http://sci-hub.tw/',
            ],
        };
    }
};
</script>

<style lang="scss">
.sci {
    .links{
        font-size: 15px;
        padding-top: 10px;
        display: block;
    }
}

</style>
