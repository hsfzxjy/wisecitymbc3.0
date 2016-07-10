<template>
    <template></template>
</template>

<script>
    export default {
        props: {
            params: {
                type: Object,
                default: {}
            },
            model: {
                type: Array,
                required: true,
                twoWay: true
            },
            url: {
                type: String,
                required: true
            }
        },
        methods: {
            load () {
                this.$http
                    .get(this.url, { params: this.params })
                    .then(res => this.model = res.data.results)
            }
        },
        events: {
            ['ListLoader:reload'] () {
                this.load()
            }
        }
    }
</script>