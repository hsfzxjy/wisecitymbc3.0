<template>
    <div>
        <div v-if="type === 'inf'">
            <infinite-loading
                :on-infinite="onInfinite">
                <div slot="no-results">
                    <slot name="no-results">no results</slot>
                </div>
                <div slot="no-more">
                    <slot name="no-more"># 已经到最后了 #</slot>
                </div>
            </infinite-loading>
        </div>
        <div v-if="type === 'pager'">
            <pager
                :has-next="hasNext"
                :has-prev="hasPrev"
                :is-loading="isLoading"
                :is-no-results="isNoResults"
                @prev="$emit('List:prev')"
                @next="$emit('List:next')">
                <div slot="no-results">
                    <slot name="no-results">空空如也～～</slot>
                </div>
            </pager>
        </div>
        <div v-if="type === 'once'">
            <slot name="no-results"></slot>
        </div>
    </div>
</template>

<script>
    import InfiniteLoading from 'vue-infinite-loading'
    import Pager from 'misc/Pager.vue'

    export default {
        components: {
            InfiniteLoading,
            Pager
        },
        data: () => ({
            page: {},
            isLoading: false
        }),
        computed: {
            hasPrev () {
                return !!this.page.previous
            },
            hasNext () {
                return !!this.page.next
            },
            isNoResults () {
                return (!this.hasNext && 
                        !this.hasPrev && (
                            _.isArray(this.page.results) &&
                            this.page.results.length === 0
                        ))
            }
        },
        props: {
            type: {
                /* inf | pager | once */
                type: String,
                default: 'inf'
            },
            model: {
                type: Array,
                required: true,
                twoWay: true
            },
            url: {
                type: String,
                required: true
            },
            params: {
                type: Object,
                default: () => ({})
            },
            autoload: {
                type: Boolean,
                default: false
            }
        },
        methods: {
            loadData (url) {
                if (this.isLoading) return

                this.isLoading = true

                return this.$http.get(url, { params: this.params })
                    .then(response => {
                        this.$set('page', response.data)
                    })
                    .then(() => {
                        this.isLoading = false
                        this.$broadcast('$InfiniteLoading:loaded')
                    })
            },
            onInfinite () {
                if (!this.hasNext) this.$broadcast('$InfiniteLoading:noMore')

                this.$emit('List:next')
            }
        },
        watch: {
            isNoResults (value) {
                if (!value) return

                if (this.type === 'inf')
                    this.$broadcast('$InfiniteLoading:noResults')
            },
            hasNext (value) {
                if (value) return

                if (this.type === 'inf')
                    this.$broadcast('$InfiniteLoading:noMore')
            }
        },
        events: {
            ['List:prev'] () {
                let url = this.page.previous
                if (!url) return

                this.loadData(url)
                    .then(() => {
                        if (this.type === 'inf')
                            this.$set('model', this.page.results.concat(this.model))
                    }).then(() => {
                        if (this.type === 'pager')
                            this.$set('model', this.page.results)
                    })
            },
            ['List:next'] () {
                let url = this.page.next
                if (!url) return

                this.loadData(url)
                    .then(() => {
                        if (this.type === 'inf') {
                            this.$set('model', this.model.concat(this.page.results))
                        }
                    }).then(() => {
                        if (this.type === 'pager')
                            this.$set('model', this.page.results)
                    })
            },
            ['List:reload'] () {
                try {
                    this.$broadcast('$InfiniteLoading:reset')
                } catch (e) {}
                this.$set('page', {})
                this.isLoading = false

                this.loadData(this.url)
                    .then(() => {
                        this.$set('model', this.page.results)
                    })
            }
        },
        ready () {
            this.autoload && this.$nextTick(() => {this.$emit('List:reload')})
        }
    }
</script>