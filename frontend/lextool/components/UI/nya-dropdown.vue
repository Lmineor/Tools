<template>
    <div class="nya-dropdown" v-show-extend="show">
        <label v-if="label" :for="id">
            {{ label }}
        </label>
        <div class="search-module clearfix" v-show="itemlist.length">
            <input class="search-text"
            @keyup='search($event)' />
            <i class="eva eva-arrow-ios-downward-outline"></i>
        </div>
        <ul class="list-module" v-show="length">
            <li v-for ="(item,index) in datalist" @click="appClick(item)" :key="index">
                <span class="list-item-text">{{item.name}}</span>
            </li>
        </ul>
            <div class="tip__nodata" v-show="!length">{{nodatatext}}</div>
    </div>
</template>
 
<script>
    export default {
        data(){
            return {
                datalist:[]
            }
        },
        props:{
            'show':{//用于外部控制组件的显示/隐藏
                type:Boolean,
                default:true
            },
            'itemlist':Array,
            label:'',
            // 'placeholder':String,
            'nodatatext':String
        },
        watch:{
            itemlist:function(val){
                this.datalist = val.concat();
            }
        },
        directives:{
            'show-extend':function(el,binding,vnode){//bind和 update钩子
                let value = binding.value,searchInput = null;
                if(value){
                    el.style.display='block';
                }else{//隐藏后，恢复初始状态
                    el.style.display='none';
                    searchInput = el.querySelector(".search-text");
                    searchInput.value = '';
                    vnode.context.datalist = vnode.context.itemlist;//还原渲染数据
                    }
            }
        },
        methods:{
            appClick:function(data){
                this.$emit('item-click',data);
            },
            search:function(e){
                let vm = this,searchvalue = e.currentTarget.value;
                vm.datalist = vm.itemlist.filter(function(item,index,arr){
                    return item.name.indexOf(searchvalue) != -1;
                });
            }
        },
        computed:{
            length:function(){
                return this.datalist.length;
            }
        }
    }
</script>
 
<style lang="scss">
.nya-dropdown {
    position: relative;
    display: inline-table;
    &.fullwidth {
        width: 100%;
    }
    &._self-show {
        display: block!important;
    }
    label {
        display: block;
        font-size: 18px;
        margin-bottom: 10px;
        font-weight: bold;
    }

    .search-module {
        position: relative;
        .search-text {
            height: 30px;
            width: 100%;
            border-radius: 0.5em;
            box-shadow: none;
            border: 1px solid #ccc;
            &:focus {
                border-color: #2198f2;
            }
        }
    }
    i {
        z-index: 1;
        line-height: 18px;
        pointer-events: none;
        position: absolute;
        right: 4px;
        bottom: 4px;
        display: flex;
        align-items: center;
        padding-right: 7px;
        font-size: 30px;
        height: calc(100% - 8px);
        box-sizing: border-box;
    }
    .list-module {
        max-height: 200px;
        overflow-y: auto;
        li {
            padding: 0px;
            list-style: none;
            &._self-hide {
                display: none;
            }
            // padding: 0.5em;
            &:hover {
                cursor:pointer;
                color: rgb(58, 56, 56);
                background: #c4c6c7;
            }
        }
    }
    .tip__nodata {
        font-size: 12px;
        margin-top: 1em;
    }
}

</style>