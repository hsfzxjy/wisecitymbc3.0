export default {
    isDigits (str) {
        return /^\d+$/.test(str)
    },
    isContainedBy (str, collections) {
        return _.indexOf(collections, str) >= 0
    },
    randStr () {
        return Math.floor((1 + Math.random()) * 0x10000).toString(16)
    }
}