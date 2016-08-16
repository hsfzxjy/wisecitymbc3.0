import Vuex from 'vuex'

import perms from './perms'

Vue.use(Vuex)

export default new Vuex.Store({
    mutations: {
        INIT_LOADING_STATE (state, path) {
            Vue.$set(state, path, true)
        },
        RESET_LOADING_STATE (state, path) {
            Vue.$set(state, path, false)
        }
    },
    modules: {
        auth
    }
})