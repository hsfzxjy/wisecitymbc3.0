export default {
    methods: {
        reset () {
            this.objects = []
            this.nextURL = ''
            this.$nextTick(() => {
                this.$broadcast('$InfiniteLoading:reset')
            })
            
        },
        load () {
            if (this.nextURL === '') 
                this.nextURL = this.baseURL
            this.$http.get(this.nextURL)
                .then((res) => {
                    let data = res.data

                    this.nextURL = data.next
                    if (_.isNull(this.nextURL)) {
                        this.$broadcast('$InfiniteLoading:noMore')
                    }

                    this.objects = this.objects.concat(data.results)
                }, (res) => {
                    if (res.status === 404)
                        this.$broadcast('$InfiniteLoading:noResults')
                }).then(() => {
                    this.$broadcast('$InfiniteLoading:loaded')
                })
        }
    }
}