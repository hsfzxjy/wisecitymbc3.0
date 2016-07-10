<template>
    <div class="col-md-6 col-md-offset-3 col-sm-12">
        <login-form @logined="logined"></login-form>
    </div>
</template>

<script>
    import LoginForm from './LoginForm.vue'

    export default {
        components: { LoginForm },
        methods: {
            logined () {
                this.$router.go('/')

                return true
            }
        }
    }
</script>