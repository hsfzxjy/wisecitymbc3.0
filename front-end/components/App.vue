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
    import vsBase from 'vuestrap-base-components'
    import navbar from './navbar.vue'
    export default {
        components: {
            'vs-alert': vsBase.alert,
            'vs-navbar': vsBase.navbar,
            'vs-nav': vsBase.nav,
            'vs-nav-item': vsBase.navItem
        },
        data: () => ({
            show: true
        })
    }
</script>