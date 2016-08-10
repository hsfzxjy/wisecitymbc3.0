const state = {
    perms: {},
    user: null,
    isPermsLoading: false,
    isUserLoading: false
}

let mutations = {
    LOGOUT (state) {
        state.perms = {}
        state.user = null
        state.isPermsLoading = false
        state.isUserLoading = false
    },
    SET_PERMS (state, perms) {
        _.merge(state.perms, perms)
    },
    SET_USER (state, user) {
        state.user = user
    }
}

export default { state, mutations }