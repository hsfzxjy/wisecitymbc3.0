<template>
    <div class="container-fluid" id="finance-summary-container">
        <stock-item
            v-for="stock in stocks"
            :stock="stock"
            :detail="false"
            class="col-md-4">
        </stock-item>
        <future-item
            v-for="future in futures"
            :future="future"
            :detail="false"
            class="col-md-4">
        </future-item>
        <list-loader
            :model.sync="stocks"
            :params="params"
            url="/api/stocks/">
        </list-loader>
        <list-loader
            :model.sync="futures"
            :params="params"
            url="/api/futures/">
        </list-loader>
    </div>
</template>
 
<style>
    #finance-summary-container .card {
        height: 158px;
    }
</style>

<script>
    import ListLoader from 'misc/ListLoader.vue'
    import StockItem from './StockItem.vue'
    import FutureItem from './FutureItem.vue'

    export default {
        components: { ListLoader, StockItem, FutureItem },
        data: () => ({
            params: { limit: -1 },
            stocks: [],
            futures: []
        }),
        route: {
            data () {
                this.$broadcast('ListLoader:reload')
            }
        }
    }
</script>