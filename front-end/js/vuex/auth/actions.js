import { waitUntil } from 'utils'

const loadingState = {
    myInfo: false,
    perms: false
}

function wait (name) {
    return waitUntil(() => !loadingState[name])
}

function fetchMyInfo ({ dispatch }) {
    loadingState.myInfo = true
    return Vue.http.get('/api/users/me/')
        .then(res => dispatch('SET_USER', res.data), _.noop)
        .then(() => loadingState.myInfo = false)
}

export function loadMyInfo ({ state, dispatch }) {
    return wait('myInfo')
        .then(() => {
            if (_.isNull(state.auth.user)) return fetchMyInfo({ dispatch })
        })
}

export function getMyInfo ({ state, dispatch }) {
    return loadMyInfo().then(() => state.user)
}

function fetchPerms (url) {
    loadingState.perms = true

    return Vue.$http.get(url)
        .then(
            ({ data }) => dispatch('SET_PERMS', data),
            _.noop
        ).then(() => loadingState.perms = false)
}

export function initPerms ({ state, dispatch }) {
    return wait('perms')
        .then(() => fetchPerms('/api/perms/'))
        .then(() => state.perms)
}

export function getPerm ({ state, dispatch }, ...args) {

    function getPermValue () {
        return Vue.$get(state.perms, args.join('.'))
    }

    return wait('perms')
        .then(() => {
            let value = getPermValue()

            if (_.isUndefined(value)) {
                let subURL = args.join('/')

                return fetchPerms(`/api/perms/${subURL}/`)
            }
        }).then(() => getPermValue())
}