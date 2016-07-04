import VueRouter from 'vue-router'

import Index from 'components/pages/Index.vue'
import Articles from 'components/pages/Articles.vue'
import ArticleEdit from 'components/pages/ArticleEdit.vue'
import ArticleDetail from 'components/pages/ArticleDetail.vue'
import Profile from 'components/pages/Profile.vue'
import Companies from 'components/pages/Companies.vue'
import Notifications from 'components/pages/Notifications.vue'
import Topics from 'components/pages/Topics.vue'
import TopicEdit from 'components/pages/TopicEdit.vue'
import TopicDetail from 'components/pages/TopicDetail.vue'

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
        '/detail/articles/:id/': {
            component: ArticleDetail
        },
        '/edit/articles/': {
            component: ArticleEdit
        },
        '/edit/articles/:id/': {
            component: ArticleEdit
        },
        '/me/': {
            component: Profile,
            id: 'me'
        },
        '/users/:id/': {
            component: Profile
        },
        '/companies/': {
            component: Companies
        },
        '/n/': {
            component: Notifications
        },
        '/topics/': {
            component: Topics
        },
        '/edit/topics/': {
            component: TopicEdit
        },
        '/edit/topics/:id/': {
            component: TopicEdit
        },
        '/detail/topics/:id/': {
            component: TopicDetail
        }
    })

    router.beforeEach(() => {
        window.scrollTo(0, 0)
    })

    return router
}