<template>
    <div class="panel" icon="person-outline">
        <div class="login-text">
            <a href="https://github.com/Prolht/Tools" target="_blank" rel="noopener noreferrer" style="color: rgb(0,0,0);">Powered by Lex吐司</a>
            <a>{{$store.state.user}}</a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Panel'
};
</script>

<style lang="scss">
.panel {
    box-sizing: border-box;
    border-radius: 50px;
    margin: 0 auto;
    margin-top: 5px;
}
</style>
