<template>
    <future-item
        v-if="list"
        v-for="item in list"
        :model="item">
    </future-item>
    <list
        :model.sync="list"
        type="pager"
        url="/api/futures/">
    </list>
</template>

<script>
    import FutureItem from './FutureItem.vue'

    export default {
        components: { FutureItem },
        data: () => ({
            list: []
        })
    }
</script>