export function isDigits (str) {
    return /^\d+$/.test(str)    
}

export function isContainedBy (str, collections) {
    return _.indexOf(collections, str) >= 0
}

export function randStr () {
    return Math.floor((1 + Math.random()) * 0x10000).toString(16)
}

export function clearObject (object) {
    _.forEach(object, (value, key) => {
        if (_.isArray(value))
            object[key] = []
        else if (_.isObject(value))
            object[key] = {}
        else if (_.isNumber(value))
            object[key] = 0
        else if (_.isBoolean(value))
            object[key] = false
        else
            object[key] = ''
    })
}

/**
 * Return a Promise, which will be resolved when condition is true.
 *
 * @param      {Function}  condition  The condition
 */
export function waitUntil (condition) {
    return Promise((resolve) => {
        function wait () {
            setTimeout(() => condition() ? resolve() : wait(), 0)
        }

        wait()
    })
}