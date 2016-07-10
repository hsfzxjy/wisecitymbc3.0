<template>
    <div class="col-xs-12 no-padding">
        <h3>
            <a v-link="'/finance/stocks/'">股票</a>
        </h3>
        <stock-item
            v-for="stock in stocks"
            :stock="stock"
            class="col-xs-12 col-md-6 small-padding">
        </stock-item>
        <list-loader
            :params="{ limit: 3 }"
            :model.sync="stocks"
            url="/api/stocks/">
        </list-loader>
    </div>

    <div class="col-xs-12 no-padding">
        <h3>
            <a v-link="'/finance/bonds/'">债券</a>
        </h3>
        <bond-item
            v-for="bond in bonds"
            :bond="bond"
            class="col-xs-12 col-md-6 small-padding">
        </bond-item>
        <list-loader
            :params="{ limit: 3 }"
            :model.sync="bonds"
            url="/api/bonds/">
        </list-loader>
    </div>

    <div class="col-xs-12 no-padding">
        <h3>
            <a v-link="'/finance/futures/'">期货</a>
        </h3>
        <future-item
            v-for="future in futures"
            :future="future"
            class="col-xs-12 col-md-6 small-padding">
        </future-item>
        <list-loader
            :params="{ limit: 3 }"
            :model.sync="futures"
            url="/api/futures/">
        </list-loader>
    </div>
</template>

<style scoped>
    h3 a {
        display: block;
    }
</style>

<script>
    import ListLoader from 'misc/ListLoader.vue'
    import StockItem from './StockItem.vue'
    import BondItem from './BondItem.vue'
    import FutureItem from './FutureItem.vue'

    export default {
        components: { ListLoader, StockItem, BondItem, FutureItem },
        data: () => ({
            stocks: [],
            bonds: [],
            futures: []
        }),
        route: {
            data (transition) {
                this.$broadcast('ListLoader:reload')
            }
        }
    }
</script>