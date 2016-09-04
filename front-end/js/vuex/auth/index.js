const state = {
    perms: {},
    user: null
}

let mutations = {
    LOGOUT (state) {
        state.perms = {}
        state.user = null
    },
    SET_PERMS (state, perms) {
        state.perms = _.merge({}, _.merge(state.perms, perms))
        Vue.set(state.perms, '_loaded', true)
    },
    SET_USER (state, user) {
        state.user = user
    }
}

export default { state, mutations }