<template>
    <stock-item
        v-if="list"
        v-for="item in list"
        :model="item">
    </stock-item>
    <list
        :model.sync="list"
        url="/api/stocks/"
        type="pager">
    </list>
</template>

<script>
    import StockItem from './StockItem.vue'

    export default {
        components: { StockItem },
        data: () => ({
            list: []
        })
    }
</script>