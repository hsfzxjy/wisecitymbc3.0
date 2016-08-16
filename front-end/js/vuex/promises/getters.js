import { isThenable, waitUntil } from 'utils'

export function getPromise ({ state }, name) {
    let promise = state.pormises[name]

    if (!isThenable(promise)) {
        /* Resolve when the promise was initialized */
        return waitUntil(() => isThenable(state.pormises[name]))
            .then(() => state.pormises[name])
    } else return promise

}