<template>
    <stock-item
        v-if="page.results"
        v-for="item in page.results"
        :stock="item">
    </stock-item>
    <pager
        :model.sync="page"
        url="/api/stocks/">
    </pager>
</template>

<script>
    import Pager from 'misc/Pager.vue'
    import StockItem from './StockItem.vue'

    export default {
        components: { Pager, StockItem },
        data: () => ({
            page: {}
        })
    }
</script>