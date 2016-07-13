import InfiniteLoading from 'vue-infinite-loading'

export default {
    components: { InfiniteLoading },
    events: {
        ['InfiniteLoading:reset'] () {
            this.reset()
        }
    },
    methods: {
        reset () {
            this[this.$options.listConfig.listFieldName] = []
            this.nextURL = ''
            this.$nextTick(() => {
                this.$broadcast('$InfiniteLoading:reset')
            })
        },
        load () {
            let url, params

            if (this.nextURL === '') {
                url = this.nextURL = this.baseURL
                params = this.params
            } else {
                url = this.nextURL
                params = {}
            }
            this.$http.get(url, { params })
                .then((res) => {
                    let data = res.data

                    this.nextURL = data.next
                    if (_.isNull(this.nextURL)) {
                        this.$broadcast('$InfiniteLoading:noMore')
                    }

                    let list = this[this.$options.listConfig.listFieldName].concat(data.results)
                    this[this.$options.listConfig.listFieldName] = _.uniq(list, 'id')
                }, (res) => {
                    if (res.status === 404)
                        this.$broadcast('$InfiniteLoading:noResults')
                }).then(() => {
                    this.$broadcast('$InfiniteLoading:loaded')
                    if (this.once)
                        this.$broadcast('$InfiniteLoading:noResults')
                })
        }
    }
}