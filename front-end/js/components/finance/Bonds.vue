<template>
    <bond-item
        v-if="page.results"
        v-for="item in page.results"
        :bond="item">
    </bond-item>
    <pager
        :model.sync="page"
        url="/api/bonds/">
    </pager>
</template>

<script>
    import Pager from 'misc/Pager.vue'
    import BondItem from './BondItem.vue'

    export default {
        components: { Pager, BondItem },
        data: () => ({
            page: {}
        })
    }
</script>