import VueRouter from 'vue-router'

import Index from '../components/pages/Index.vue'
import Articles from '../components/pages/Articles.vue'
import ArticleEdit from '../components/pages/ArticleEdit.vue'

export default function (Vue) {
    Vue.use(VueRouter)

    let router = new VueRouter({
        saveScrollPosition: true
    })

    router.map({
        '/': {
            component: Index
        },
        '/articles/:category/': {
            component: Articles,
            name: 'articlesList'
        },
        '/articlesEdit/': {
            component: ArticleEdit
        }
    })

    router.beforeEach(() => {
        window.scrollTo(0, 0)
    })

    return router
}