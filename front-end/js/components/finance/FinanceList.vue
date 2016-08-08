<template>
    <div>
        <component
            :is="itemComponent"
            v-for="item in list"
            :model.sync="item">
        </component>
        <list
            :model.sync="list"
            type="pager"
            :url="'/api/'+product+'/'"
            autoload>
        </list>
    </div>
</template>

<script>
    import StockItem from './StockItem.vue'
    import BondItem from './BondItem.vue'
    import FutureItem from './FutureItem.vue'

    export default {
        data: () => ({
            itemComponent: '',
            product: '',
            list: []
        }),
        components: { StockItem, BondItem, FutureItem },
        route: {
            data ({ to, next }) {
                let product = to.params.product

                next({ 
                    product,
                    itemComponent: {
                        stocks: 'StockItem',
                        bonds: 'BondItem',
                        futures: 'FutureItem'
                    }[product]
                })
            }
        }
    }
</script>