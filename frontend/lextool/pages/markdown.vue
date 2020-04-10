<template>
    <div class="markdown">
        <nya-container title="markdown">
        </nya-container>
            <div class="markdown">
                <Markdown/>
            </div>
        <nya-container v-if="res" title="结果">
            <div v-html="res"></div>
        </nya-container>
    </div>
</template>


<script>
import MarkdownPro from '@/components/mk/pro';
import MarkdownPreview from '@/components/mk/preview';

export default {
        name: "markdown",
        components: {
            MarkdownPro,
            MarkdownPreview,
        }
    }
</script>
