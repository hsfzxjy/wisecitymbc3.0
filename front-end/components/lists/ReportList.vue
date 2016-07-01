<template>
    <vs-list-group flush>
        <vs-list-group-item v-for="file in objects">
            {{ file.file_name }}
        </vs-list-group-item>
        <infinite-loading :on-infinite="load"></infinite-loading>
    </vs-list-group>
</template>

<script>
    import InfiniteLoading from 'vue-infinite-loading'
    import InfiniteLoadingMixin from 'components/mixins/InfiniteLoadingMixin.es'

    export default {
        components: { InfiniteLoading },
        mixins: [InfiniteLoadingMixin],
        data: () => ({
            objects: [],
            nextURL: ''
        }),
        props: {
            userId: {
                required: true,
                type: Number
            }
        },
        computed: {
            baseURL: {
                get () {
                    return `/api/users/${this.userId}/reports/`
                }
            }
        },
        ready () {
            this.$watch('userId', () => {
                this.reset()
            })
        }
    }
</script>