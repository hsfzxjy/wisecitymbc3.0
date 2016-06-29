import App from './components/App.vue'

require('./node_modules/bootstrap/dist/css/bootstrap.min.css')

require.ensure([], (require) => {
    let Vue = require('vue')
    let router = require('./init/routes.es').default(Vue)
    require('./init/resources.es').default(Vue)
    require('./init/filters.es').default(Vue)
    require('./init/components.es').default(Vue, () => {
        router.start(App, '#app')
    })
})