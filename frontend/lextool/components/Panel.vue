<template>
    <div class="panel" icon="person-outline">
        <div class="login-text">
            <a v-if="$store.state.user" href="https://github.com/Prolht/Tools" target="_blank" rel="noopener noreferrer" style="color: #024466;">
                {{$store.state.user}}
            </a>
            <a v-else href="https://github.com/Prolht/Tools" target="_blank" rel="noopener noreferrer" style="color: #024466;">
                (❤ ω ❤)o
            </a>
            <!-- <a>{{$store.state.user}}</a> -->
        </div>
        <!-- <div class="login-text">
            <a style="text-align: center; color:rgb(0,0,0);">{{$store.state.user}}</a>
        </div> -->
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
