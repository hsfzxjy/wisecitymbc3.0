<template>
    <div>
        <top-nav-bar></top-nav-bar>
        <div class="container-fluid" id="main-container" style="margin-top:75px;">
            <router-view class="view" keep-alive transition transition-mode="out-in">
            </router-view>            
        </div>
    </div>
</template>

<script>
    import TopNavBar from './navs/TopNavBar.vue'

    export default {
        components: {
            TopNavBar
        },
        data: () => ({
            user: null,
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