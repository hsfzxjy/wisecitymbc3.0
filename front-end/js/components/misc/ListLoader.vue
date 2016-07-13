<template>
    <span class="list-loader-wrapper">
        <slot name="loading" v-if="loading">
            <span>加载中 ...</span>
        </slot>
        <slot name="no-results" v-if="noResults">
            <span class="list-loader-no-results">空空如也～～</span>
        </slot>
    </span>
</template>

<style scoped>
    .list-loader-wrapper {
        display: block;
        text-align: center;
    }
</style>

<script>
    export default {
        data: () => ({
            loading: false,
            noResults: false
        }),
        props: {
            params: {
                type: Object,
                default: () => ({})
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
            init () {
                this.loading = false
                this.noResults = false
            },
            load () {
                this.$http
                    .get(this.url, { params: this.params })
                    .then(res => {
                        this.model = res.data.results
                        if (!this.model.length)
                            this.$emit('ListLoader:no-results')
                    })
            }
        },
        events: {
            ['ListLoader:reload'] () {
                this.init()
                this.load()
            },
            ['ListLoader:no-results'] () {
                this.noResults = true
            }
        }
    }
</script>