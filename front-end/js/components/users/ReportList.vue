<template>
    <file-list :model.sync="reports" :base-url='baseURL' :delete-link="true">
        <list
            :url="baseURL"
            :model.sync="reports"
            autoload>
        </list>
    </file-list>
</template>

<style scoped>
    li a {
        margin: 0 .2rem;
    }
</style>

<script>
    import FileList from 'files/FileList.vue'

    export default {
        components: { FileList },
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
                return `/api/users/`+this.userId+`/reports/`
            }
        }
    }
</script>