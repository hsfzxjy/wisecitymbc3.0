<template>
    <div class="col-xs-12 sm-no-padding">
        <h3>
            <a v-link="'/finance/stocks/'">股票</a>
        </h3>
        <stock-item
            v-for="stock in stocks"
            :model="stock"
            class="col-xs-12 col-md-6 sm-no-padding">
        </stock-item>
        <list
            :params="{ limit: 3 }"
            :model.sync="stocks"
            url="/api/stocks/"
            type="once"
            autoload>
        </list>
    </div>

    <div class="col-xs-12 sm-no-padding">
        <h3>
            <a v-link="'/finance/bonds/'">债券</a>
        </h3>
        <bond-item
            v-for="bond in bonds"
            :model="bond"
            class="col-xs-12 col-md-6 sm-no-padding">
        </bond-item>
        <list
            :params="{ limit: 3 }"
            :model.sync="bonds"
            url="/api/bonds/"
            type="once"
            autoload>
        </list>
    </div>

    <div class="col-xs-12 sm-no-padding">
        <h3>
            <a v-link="'/finance/futures/'">期货</a>
        </h3>
        <future-item
            v-for="future in futures"
            :model="future"
            class="col-xs-12 col-md-6 sm-no-padding">
        </future-item>
        <list
            :params="{ limit: 3 }"
            :model.sync="futures"
            url="/api/futures/"
            type="once"
            autoload>
        </list>
    </div>
</template>

<style scoped>
    h3 a {
        display: block;
    }
</style>

<script>
    import StockItem from './StockItem.vue'
    import BondItem from './BondItem.vue'
    import FutureItem from './FutureItem.vue'

    export default {
        components: { StockItem, BondItem, FutureItem },
        data: () => ({
            stocks: [],
            bonds: [],
            futures: []
        })
    }
</script>