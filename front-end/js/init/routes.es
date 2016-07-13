import VueRouter from 'vue-router'

import Index from "pages/Index.vue"
import Login from "auth/Login.vue"
import Logout from "auth/Logout.vue"
import Articles from "articles/Articles.vue"
import Tags from "articles/Tags.vue"
import ArticleDetail from "articles/ArticleDetail.vue"
import ArticleEdit from "articles/ArticleEdit.vue"
import Profile from "users/Profile.vue"
import Companies from "users/Companies.vue"
import Notifications from "notifications/Notifications.vue"
import Topics from "questions/Topics.vue"
import TopicEdit from "questions/TopicEdit.vue"
import TopicDetail from "questions/TopicDetail.vue"
import Finance from "finance/Finance.vue"
import FinanceIndex from "finance/FinanceIndex.vue"
import Stocks from 'finance/Stocks.vue'
import Bonds from 'finance/Bonds.vue'
import Futures from 'finance/Futures.vue'
import RAM from 'finance/RAM.vue'
import NotFound from "pages/404.vue"

export default function (Vue) {
    Vue.use(VueRouter)

    let router = new VueRouter({
        saveScrollPosition: true
    })

    router.map({
        '/': {
            component: Index,
            name: 'index'
        },
        '/login/': {
            component: Login,
            name: 'login'
        },
        '/logout/': {
            component: Logout,
            name: 'logout'
        },
        '/articles/:category/': {
            component: Articles,
            name: 'article-list'
        },
        '/tags/': {
            component: Tags,
            name: 'tag-list'
        },
        '/tags/:id/': {
            component: Tags,
            name: 'tag-detail'
        },
        '/detail/articles/:id/': {
            component: ArticleDetail,
            name: 'article-detail'
        },
        '/edit/articles/': {
            component: ArticleEdit,
            name: 'article-add',
            auth: {
                model: 'articles.article',
                action: 'add'
            }
        },
        '/edit/articles/:id/': {
            component: ArticleEdit,
            name: 'article-edit',
            auth: {
                model: 'articles.article',
                action: 'change'
            }
        },
        '/me/': {
            component: Profile,
            name: 'user-me',
            id: 'me',
            auth: {
                login: true
            }
        },
        '/users/:id/': {
            component: Profile,
            name: 'user-detail'
        },
        '/companies/': {
            component: Companies,
            name: 'user-list-companies'
        },
        '/n/': {
            component: Notifications,
            name: 'notification-list',
            auth: {
                login: true
            }
        },
        '/topics/': {
            component: Topics,
            name: 'topic-list',
            auth: {
                model: 'questions.topic',
                action: 'view'
            }
        },
        '/edit/topics/': {
            component: TopicEdit,
            name: 'topic-add',
            auth: {
                model: 'questions.topic',
                action: 'add'
            }
        },
        '/edit/topics/:id/': {
            component: TopicEdit,
            name: 'topic-edit',
            auth: {
                model: 'questions.topic',
                action: 'change'
            }
        },
        '/detail/topics/:id/': {
            component: TopicDetail,
            name: 'topic-detail',
            auth: {
                model: 'questions.topic',
                action: 'view'
            }
        },
        '/finance': {
            component: Finance,
            subRoutes: {
                '/': {
                    component: FinanceIndex,
                    name: 'finance-index'
                },
                '/stocks/': {
                    component: Stocks,
                    name: 'stock-list'
                },
                '/bonds/': {
                    component: Bonds,
                    name: 'bond-list'
                },
                '/futures/': {
                    component: Futures,
                    name: 'futures-list'
                }
            }
        },
        '/ram/': {
            component: RAM,
            name: 'ram-index'
        },
        '*': {
            component: NotFound
        }
    })

    router.beforeEach(function ({ to, next, redirect }) {
        if (to.auth) {
            if (to.auth.login) {
                return router.app.checkLogined()
            } else
                return router.app.getPerm(
                    to.auth.model,
                    to.auth.action,
                    parseInt(to.params.id) || undefined
                )
        } else next()
    })

    router.beforeEach(() => {
        window.scrollTo(0, 0)
    })

    return router
}