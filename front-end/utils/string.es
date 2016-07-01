import _ from 'lodash'

export default {
    isDigits (str) {
        return /^\d+$/.test(str)
    },
    isContainedBy (str, collections) {
        return _.indexOf(collections, str) >= 0
    }
}