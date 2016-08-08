export default function (Vue, callback) {
    require.ensure([], (require) => {
        let vsBase = require('vuestrap-base-components')

        _.forEach(vsBase, (component, name) => {
            Vue.component('vs-'+_.kebabCase(name), component)
        })

        let vsFormButton = require('vs-extend/form-button.vue')
        let vsExpansion = require('vs-extend/expansion.vue')
        let Editable = require('vs-extend/Editable.vue')
        let BlockA = require('vs-extend/BlockA.vue')
        let vsForm = require('vs-extend/form.vue')

        let SideBar = require('vue-strap/src/Aside.vue')
        let List = require('misc/List.vue')

        Vue.component('vs-form-button', vsFormButton)
        Vue.component('vs-expansion', vsExpansion)
        Vue.component('vs-form', vsForm)
        Vue.component('vs-link', BlockA)
        Vue.component('sidebar', SideBar)
        Vue.component('editable', Editable)
        Vue.component('List', List)

        callback()
    })
}