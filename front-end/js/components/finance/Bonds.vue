<template>
    <bond-item
        v-if="list"
        v-for="item in list"
        :model="item">
    </bond-item>
    <list
        :model.sync="list"
        type="pager"
        url="/api/bonds/">
    </list>
</template>

<script>
    import BondItem from './BondItem.vue'

    export default {
        components: { BondItem },
        data: () => ({
            list: []
        })
    }
</script>