<template>
    <!-- 参考：https://blog.csdn.net/qq_41619796/article/details/101075443 -->
    <div class="nya-dropdown" :class="{ 'fullwidth': fullwidth }">
        <label v-if="label" :for="id">
            {{ label }}
        </label>
        <Select 
            :clearable="clearable"
            :multiple='multiple'
            :filterable='filterable'
            :size='size'
            :placeholder='placeholder'
            @on-change='changeFun'
        >
            <Option v-for="(item, index) in items" :key="index" :value="index">{{ item }}</Option>
        </Select>
    </div>
</template>
 
<script>
export default {
    inheritAttrs: false,
    props: {
        clearable: {//是否可以清空选项，只在单选时有效
            type: Boolean,
            default: true
        },  
        multiple: { //是否支持多选
            type: Boolean,
            default: false
        }, 
        filterable: { //是否支持搜索,多选搜索时，可以使用键盘Delete快捷删除最后一个已选项
            type: Boolean,
            default: true
        },
        size: String, //选择框大小，可选值为large、small、default或者不填
        placeholder: String, //选择框默认文字
        items: {
            default: () => {
                return [];
            },
            type: [Array, Object]
        },
        label: {
            default: '',
            type: String
        },
        fullwidth: {
            default: false,
            type: Boolean
        }
    },
    methods:{
        changeFun(data){//下拉框值发生改变时调用
            this.$emit('change',data);//data有value和label
        },
    },
    data(){
        return {
            id: null
        };
    },
    mounted() {
        // changeGrade(grade){
        //     this.gradeId = grade
        // },
        this.id = this.$shortid.generate();
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

    label {
        display: block;
        font-size: 18px;
        margin-bottom: 10px;
        font-weight: bold;
    }

}
</style>
