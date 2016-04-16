<template>
    
</template>

<script>
    import Vue from 'vue';
    import myHeader from '../components/my-header.vue';
    import myFooter from '../components/my-footer.vue';
    import splitter from '../components/splitter.vue';
    import content from '../components/content.vue';

    new Vue({
        el: '#div',
        data: {
            title: 'This is the title.'
        },
        components: { myHeader,myFooter, splitter, content }
    })
</script>