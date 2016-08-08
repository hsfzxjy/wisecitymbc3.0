<template>
    <div class="container-fluid" id="finance-summary-container">
        <stock-item
            v-for="stock in stocks"
            :model="stock"
            :detail="false"
            class="col-md-4">
        </stock-item>
        <future-item
            v-for="future in futures"
            :model="future"
            :detail="false"
            class="col-md-4">
        </future-item>
        <list
            :model.sync="stocks"
            :params="params"
            url="/api/stocks/"
            type="once"
            autoload>
        </list>
        <list
            :model.sync="futures"
            :params="params"
            url="/api/futures/"
            type="once"
            autoload>
        </list>
    </div>
</template>
 
<style>
    #finance-summary-container .card {
        height: 158px;
    }
</style>

<script>
    import StockItem from './StockItem.vue'
    import FutureItem from './FutureItem.vue'

    export default {
        components: { StockItem, FutureItem },
        data: () => ({
            params: { limit: -1 },
            stocks: [],
            futures: []
        })
    }
</script>