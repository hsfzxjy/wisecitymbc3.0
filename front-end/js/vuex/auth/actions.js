import waitUntil from 'utils'

import { getPromise } from 'vuex/promises/getters'

export function loadMyInfo ({ state, dispatch }) {
    let promise = Vue.$http.get('/api/users/me/')
        .then(res => dispatch('SET_USER', res.data))

    dispatch('SET_PROMISE', promise)
    return promise
}

export function initPerms ({ state, dispatch }) {
    if (state.isPermsLoading) {
        return waitUntil(() => !state.isPermsLoading).then(() => state.perms)
    } else {
        return fetchPerms('/api/perms/').then(() => state.perms)
    }
}

export function getMyInfo ({ state, dispatch }) {
    return waitUntil(() => !state.isUserLoading).then(() => state.user)
}

export function getPerm ({ state, dispatch }, ...args) {

    function get () {
        return Vue.$get(state.perms, args.join('.'))
    }

    return waitUntil(() => !state.isPermsLoading).then(() => {
        if (!_.isUndefined(get())) return permValue

        let subURL = args.concat(['']).join('/')
        return fetchPerms(`/api/perms/${subURL}/`)
            .then(() => get())
    })
}

function fetchPerms (url) {
    dispatch('INIT_LOADING_STATE', 'auth.isPermsLoading')
    return Vue.$http.get(url)
        .then(
            ({ data }) => dispatch('SET_PERMS', data), 
            () => dispatch('SET_PERMS', {})
        )
}