<template>
    <div id="login-page" class="clearfix">
        <div class="carousel-wrapper">
            <div class="carousel slide" data-interval="5000" data-ride="carousel">
                <div class="carousel-inner">
                    <div
                        class="carousel-item {{index===1 && 'active'}}"
                        v-for="index in [1,2,3,4,5]">
                        <img :src="'/static/carousel/'+index+'.jpg'">
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-md-offset-3 col-sm-12 login-form-wrapper">
            <login-form @logined="logined" class="login-form"></login-form>
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
        overflow: hidden;
    }

    .login-form {
        z-index: 21000;
    }

    .login-form-wrapper {
        margin-top: 4rem;
    }
    
    .carousel-wrapper {
        position: absolute;
    }

    .carousel {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        min-height: 100%;
        opacity: .2;
    }

    .carousel img {
        display: block;
        width: 100%;
        min-height: 100%;
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