<template>
    <div></div>
</template>

<script>
    export default {
        route: {
            data (transition) {
                return this.$http.get('/api/users/logout/')
                    .then(res => {
                        this.$root.$emit('logout')
                        this.$root.$broadcast('logout')
                        transition.redirect(transition.from.path || '/')
                    })
            }
        }
    }
</script>