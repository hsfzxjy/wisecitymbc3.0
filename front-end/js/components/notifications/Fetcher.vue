<template>
    <template></template>
</template>

<script>
    import { checkHasLogined } from 'vuex/auth/actions'
    import store from 'vuex/store'

    export default {
        ready () {
            this.fetch()
        },
        methods: {
            fetch () {
                checkHasLogined(store)
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