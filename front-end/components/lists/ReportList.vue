<template>
    <vs-list-group flush>
        <vs-list-group-item v-for="file in reports">
            {{ file.file_name }}
        </vs-list-group-item>
        <infinite-loading :on-infinite="load"></infinite-loading>
    </vs-list-group>
</template>

<script>
    import InfiniteLoadingMixin from 'components/mixins/InfiniteLoadingMixin.es'

    export default {
        mixins: [InfiniteLoadingMixin],
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