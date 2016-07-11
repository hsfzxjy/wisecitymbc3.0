<template>
    <file-list :model.sync="reports" :base-url='baseURL' :delete-link="true">
        <infinite-loading :on-infinite="load"></infinite-loading>
    </file-list>
</template>

<style scoped>
    li a {
        margin: 0 .2rem;
    }
</style>

<script>
    import InfiniteLoadingMixin from 'mixins/InfiniteLoadingMixin.es'
    import FileList from 'files/FileList.vue'

    export default {
        mixins: [InfiniteLoadingMixin],
        components: { FileList },
        listConfig: {
            listFieldName: 'reports'
        },
        data: () => ({
            nextURL: ''
        }),
        props: {
            reports: {
                type: Array,
                twoWay: true,
                required: true
            },
            userId: {
                required: true,
                type: Number
            }
        },
        computed: {
            baseURL () {
                return `/api/users/${this.userId}/reports/`
            }
        },
        ready () {
            this.$watch('userId', () => {
                this.reset()
            })
        }
    }
</script>