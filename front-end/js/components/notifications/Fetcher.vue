<template>
    <template></template>
</template>

<script>
    export default {
        ready () {
            this.fetch()
        },
        methods: {
            fetch () {
                this.$root.checkLogined()
                    .then(logined => {
                        if (logined)
                            this.$http.get('/api/n/unread_count/')
                                .then(res => {
                                    this.$root.$broadcast('new-notifications', res.data.count)
                                    this.$root.$emit('new-notifications', res.data.count)
                                })
                    })
                setTimeout(this.fetch.bind(this), 1000*60*5)
            }
        }
    }
</script>