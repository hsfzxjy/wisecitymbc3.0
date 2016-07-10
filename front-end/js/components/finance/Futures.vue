<template>
    <future-item
        v-if="page.results"
        v-for="item in page.results"
        :future="item">
    </future-item>
    <pager
        :model.sync="page"
        url="/api/futures/">
    </pager>
</template>

<script>
    import Pager from 'misc/Pager.vue'
    import FutureItem from './FutureItem.vue'

    export default {
        components: { Pager, FutureItem },
        data: () => ({
            page: {}
        })
    }
</script>