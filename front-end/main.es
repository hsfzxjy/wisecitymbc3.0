import App from './components/App.vue'
import Index from './components/pages/Index.vue'

require('./node_modules/bootstrap/dist/css/bootstrap.min.css')

require.ensure(['vuestrap-base-components'], (require) => {
    let Vue = require('vue')
    let Router = require('vue-router')
    let VueResource = require('vue-resource')

    Vue.use(Router)
    Vue.use(VueResource)
    Vue.http.options.root = '/api'
    Vue.http.headers.common['X-CSRFToken'] = /csrftoken=(.*)(\s|;|$)/.exec(document.cookie)[1]

    let router = new Router({
        //history: true,
        saveScrollPosition: true,
    })

    router.map({
        '/': {
            component: Index
        }
    })

    router.beforeEach(() => {
        window.scrollTo(0, 0)
    })

    router.start(App, '#app')
})