<template>
    <div id="login-page" class="clearfix">
        <div class="col-md-6 col-md-offset-3 col-sm-12">
            <login-form @logined="logined"></login-form>
        </div>        
    </div>
</template>

<style scoped>
    #login-page {
        position: fixed;
        z-index: 20000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: #1f2324;
        padding-top: 50px;
    }
</style>

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