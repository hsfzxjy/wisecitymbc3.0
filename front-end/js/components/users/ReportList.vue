<template>
    <vs-list-group flush>
        <vs-list-group-item v-for="file in reports">
            {{ file.file_name }}
            <a
                href="#"
                class="pull-xs-right"
                @click.stop.prevent="removeFile($index)">
                删除
            </a>
        </vs-list-group-item>
        <infinite-loading :on-infinite="load"></infinite-loading>
    </vs-list-group>
</template>

<script>
    import InfiniteLoadingMixin from 'mixins/InfiniteLoadingMixin.es'

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
        },
        methods: {
            removeFile (index) {
                this.reports.splice(index, 1)
            }
        }
    }
</script>