import App from './components/App.vue'
import Router from 'init/routes.es'

let router = Router(Vue)

import ResourceInit from 'init/resources.es'
import FilterInit from 'init/filters.es'
import ComponentInit from 'init/components.es'

ResourceInit(Vue)
FilterInit(Vue)
ComponentInit(Vue, () => {
    router.start(App, '#app')
})

require('styles/bootstrap.scss') 
require('font-awesome-sass-loader!font-awesome.config.js')