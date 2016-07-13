<template>
    <div>
        <slot name="no-results" v-if="noResults">
            <p class="text-xs-center">空空如也～～</p>
        </slot>
        <slot name="loading" v-if="loading">
            <p class="text-xs-center">加载中...</p>
        </slot>
        <vs-pager v-if="model">
            <li v-show="model.previous" :class="!loading || 'disabled'">
                <a @click.stop="load(model.previous)" href="javascript:void(0);">上一页</a>
            </li>
            <li v-show="model.next" :class="!loading || 'disabled'">
                <a @click.stop="load(model.next)" href="javascript:void(0);">下一页</a>
            </li>
        </vs-pager>        
    </div>
</template>

<style scoped>
    p.text-xs-center {
        padding: .75rem 0;
    }
</style>

<script>
    export default {
        data: () => ({
            loading: false,
            noResults: false
        }),
        props: {
            model: {
                type: Object,
                twoWay: true,
                required: true
            },
            url: {
                type: String,
                required: true
            }
        },
        ready () {
            this.refresh()
        },
        methods: {
            load (url) {
                this.$http.get(url)
                    .then(res => {
                        this.model = res.data
                        this.noResults = !res.data.results.length
                        console.log(this.model, this.noResults)
                    })
            },
            refresh () {
                this.loading = false
                this.noResults = false
                this.model.results = []
                this.load(this.url)
            }
        },
        events: {
            ['Pager:refresh'] () {
                this.refresh()
            }
        },
        watch: {
            url (value) {
                this.refresh()
            }
        }
    }
</script>