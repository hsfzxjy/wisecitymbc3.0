<template>
    <div>
    <vs-jumbotron fluid>
        <div class="col-md-8 hidden-sm-down">
            <h1 class="display-3">
                WiseCity
            </h1>
        </div>
        <div class="col-md-4 col-sm-12">
            <login-form></login-form>
        </div>
    </vs-jumbotron>
    </div>
</template>

<script>
    import LoginForm from '../forms/LoginForm.vue'
    import vsBase from 'vuestrap-base-components'

    export default {
        components: {
            LoginForm,
            'vs-jumbotron': vsBase.jumbotron
        }
    }
</script>