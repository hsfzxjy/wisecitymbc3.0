import _ from 'lodash'

export default function (Vue) {
    Vue.filter('state', (value) => _.isEmpty(value) ? '' : 'danger')
}