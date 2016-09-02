<template>
    <div>
        <top-nav-bar></top-nav-bar>
        <notification-fetcher></notification-fetcher>
        <sidebar :show.sync="showSideBar" placement="right" header="WiseCity" :width="350"
            style="max-width: 100%;">
            <side-bar-content></side-bar-content>
        </sidebar>
        <div class="container-fluid" id="main-container">
            <router-view
                class="view" 
                keep-alive 
                transition="fade"
                transition-mode="out-in">
            </router-view>            
        </div>
    </div>
</template>

<script>
    import TopNavBar from 'navs/TopNavBar.vue'
    import SideBarContent from 'misc/SideBarContent.vue'
    import NotificationFetcher from 'notifications/Fetcher.vue'

    import store from 'vuex/store'
    import { auth as authActions } from 'vuex/actions'

    export default {
        components: {
            TopNavBar,
            SideBarContent,
            NotificationFetcher
        },
        data: () => ({
            showSideBar: false,
            nCount: 0
        }),
        methods: {
            refreshCurrentView () {
                this.$broadcast('List:reload')
            }
        },
        vuex: {
            actions: {
                loadMyInfo: authActions.loadMyInfo
            },
            getters: {
                user (state) {
                    return state.auth.user
                }
            }
        },
        created () {
            this.loadMyInfo()
        },
        events: {
            ['new-notifications'] (count) {
                this.nCount = count
                return true
            }
        },
        store
    }
</script>