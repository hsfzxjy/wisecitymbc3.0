<template>
    <div>
        <top-nav-bar></top-nav-bar>
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

    export default {
        components: {
            TopNavBar,
            SideBarContent
        },
        data: () => ({
            user: null,
            perms: {},
            showSideBar: false,
            initPromise: null
        }),
        computed: {
            hasLogined () {
                return !!this.user
            }
        },
        methods: {
            _getName (model, action, id) {
                return [model.replace('.', '_'), action, (id || '')].join('_')
            },
            _extendPerms (perms) {
                _.forEach(perms, (value, key) => {
                    this.$set('perms.'+key, value)
                })
            },
            _loadAddPerms () {
                return this.$http.get('/api/perms/')
                    .then(res => this._extendPerms(res.data))
            },
            loadPerms (model, id) {
                return this.$http.get(`/api/object_perms/${model}/${id}/`)
                    .then(res => this._extendPerms(res.data, id))
            },
            getPerm (model, action, id) {
                return this.initPromise.then(() => {
                    let name = this._getName(model, action, id)
                    console.log(name)

                    if (!_.isUndefined(this.perms[name]))
                        return this.perms[name]
                    else
                        return this.loadPerms(model, id)
                            .then(() => this.perms[name], () => false)
                })
            },
            resetPerms () {
                this.perms = {}
                this.reseting = false
                return this._loadAddPerms().then(() => this.reseting = false)
            },
            checkLogined () {
                return this.initPromise
                    .then(() => this.hasLogined)
            }
        },
        created () {
            return this.initPromise = Promise.all([
                this.$http.get('/api/users/me/'),
                this.resetPerms()
            ]).then(([userRes]) => {
                this.user = userRes.data
            }, _.noop)
        },
        events: {
            logined (user) {
                this.user = user
                this.initPromise = this.resetPerms()

                return true
            },
            logout () {
                this.user = null
                this.initPromise = this.resetPerms()

                return true
            }
        }
    }
</script>