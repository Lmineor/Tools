<template>
    <div class="markdown">
        <mavon-editor 
            v-model="handbook"
            @save="$save"
        >
        </mavon-editor>
    </div>
</template>


<script>

import { mavonEditor } from 'mavon-editor'
import createFile from  '~/utils/createFile.js';
import handbooks from '~/utils/handbook.js';

export default {
    head() {
        return {
            title: 'Markdown编辑器'
        };
    },
    data() {
        return {
            // handbook: "#### 开始使用"
            handbook: handbooks.content
        };
    },
    methods:{
        $save(val, render){
            createFile(val, 'markdown.md');
        }
    },
}
</script>
