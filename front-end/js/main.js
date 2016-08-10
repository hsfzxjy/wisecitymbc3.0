global.Promise = Vue.Promise
global.consts = require('./consts.json')

import App from './components/App.vue'
import Router from 'init/routes'

let router = Router(Vue)

import ResourceInit from 'init/resources'
import FilterInit from 'init/filters'
import ComponentInit from 'init/components'

ResourceInit(Vue)
FilterInit(Vue)
ComponentInit(Vue, () => {
    router.start(App, '#app')
})

require('styles/bootstrap.scss') 
require('font-awesome-sass-loader!font-awesome.config.js')