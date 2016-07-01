import VueRouter from 'vue-router'

import Index from '../components/pages/Index.vue'
import Articles from '../components/pages/Articles.vue'
import ArticleEdit from '../components/pages/ArticleEdit.vue'
import ArticleDetail from '../components/pages/ArticleDetail.vue'
import Profile from 'components/pages/Profile.vue'

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
        '/articleDetail/:id/': {
            component: ArticleDetail
        },
        '/articlesEdit/': {
            component: ArticleEdit
        },
        '/me/': {
            component: Profile,
            id: 'me'
        },
        '/users/:id/': {
            component: Profile
        }
    })

    router.beforeEach(() => {
        window.scrollTo(0, 0)
    })

    return router
}