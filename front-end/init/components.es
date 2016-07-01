//import vsBase from 'vuestrap-base-components'
import _ from 'lodash'

export default function (Vue, callback) {
    require.ensure([], (require) => {
        let vsBase = require('vuestrap-base-components')

        _.forEach(vsBase, (component, name) => {
            Vue.component('vs-'+_.kebabCase(name), component)
        })

        let vsFormButton = require('../components/vs-extend/form-button.vue')

        Vue.component('vs-form-button', vsFormButton)

        callback()
    })
}