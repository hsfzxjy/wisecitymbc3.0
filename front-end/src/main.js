import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App'
import Hello from './components/Hello'

Vue.use(VueRouter)

const routes = [
    { path: '/hello', component: Hello }
]

let router = new VueRouter({
    routes,
    scrollBehavior: () => ({ y: 0 })
})

const app = new Vue({
    el: 'app',
    router,
    ...App
})

console.log(app)

export { app }
