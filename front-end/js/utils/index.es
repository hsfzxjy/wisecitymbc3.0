import StrUtils from './string.es'

export {StrUtils}

export let clearObject = function (object) {
    _.forEach(object, (value, key) => {
        if (_.isArray(value))
            object[key] = []
        else if (_.isObject(value))
            object[key] = {}
        else
            object[key] = ''
    })
}