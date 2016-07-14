import StrUtils from './string.es'

export {StrUtils}

export let clearObject = function (object) {
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