<template>
    <div>
        <vs-navbar type="light" variant="reverse" full>
            <a class="navbar-brand" href="#">Navbar</a>
            <vs-nav type="navbar" class="pull-xs-left">
                <vs-nav-item link="#" active>Home <span class="sr-only">(current)</span></vs-nav-item>
                <vs-nav-item link="#">Features</vs-nav-item>
                <vs-nav-item link="#">Pricing</vs-nav-item>
                <vs-nav-item link="#">About</vs-nav-item>
            </vs-nav>
        </vs-navbar>
        <div class="container">
            <router-view class="view" keep-alive transition transition-mode="out-in">
            </router-view>            
        </div>
    </div>
</template>

<script>
    import navbar from './navbar.vue'

    export default {
        components: {
        },
        data: () => ({
            user: null
        }),
        computed: {
            hasLogined () {
                return !!this.user
            }
        },
        ready () {
            this.$http.get('/api/users/me/').then((res) => {
                this.user = res.data
            }, (res) => {})
        },
        events: {
            logined (user) {
                this.user = user
            }
        }
    }
</script>