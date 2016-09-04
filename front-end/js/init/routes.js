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
import StockFutures from 'finance/StockFutures.vue'
import FinanceList from 'finance/FinanceList.vue'
import RAM from 'finance/RAM.vue'
import NotFound from "pages/404.vue"

import store from 'vuex/store'
import { checkHasLogined, getPerm } from 'vuex/auth/actions'

export default function (Vue) {
    Vue.use(VueRouter)

    let router = new VueRouter({
        saveScrollPosition: true
    })

    router.map({
        '/': {
            component: Index,
            name: 'index',
            title: '首页'
        },
        '/login/': {
            component: Login,
            name: 'login',
            title: '登录'
        },
        '/logout/': {
            component: Logout,
            name: 'logout',
            title: '退出登录'
        },
        '/articles/:category/': {
            component: Articles,
            name: 'article-list',
            title: function () {
                console.log(consts, this)
                return `${consts.article_type_verbose[this.params.category]}·资讯`
            },
            validator: {
                category: new RegExp(
                    '^('+_.values(consts.ArticleType).join('|')+')$'
                )
            }
        },
        '/tags/': {
            component: Tags,
            name: 'tag-list',
            title: '标签'
        },
        '/tags/:id/': {
            component: Tags,
            name: 'tag-detail',
            title: '标签'
        },
        '/detail/articles/:id/': {
            component: ArticleDetail,
            name: 'article-detail',
            title: '资讯详情'
        },
        '/edit/articles/': {
            component: ArticleEdit,
            name: 'article-add',
            title: '撰写资讯',
            auth: ['articles', 'article', 'add']
        },
        '/edit/articles/:id/': {
            component: ArticleEdit,
            name: 'article-edit',
            title: '编辑资讯',
            auth: ['articles', 'article', 'change']
        },
        '/me/': {
            component: Profile,
            name: 'user-me',
            id: 'me',
            title: '我'
        },
        '/users/:id/': {
            component: Profile,
            name: 'user-detail',
            title: '用户'
        },
        '/companies/': {
            component: Companies,
            name: 'user-list-companies',
            title: '公司'
        },
        '/n/': {
            component: Notifications,
            name: 'notification-list',
            title: '消息'
        },
        '/topics/': {
            component: Topics,
            name: 'topic-list',
            title: '问题',
            auth: ['questions', 'topic', 'view']
        },
        '/edit/topics/': {
            component: TopicEdit,
            name: 'topic-add',
            title: '提问',
            auth: ['questions', 'topic', 'add']
        },
        '/edit/topics/:id/': {
            component: TopicEdit,
            name: 'topic-edit',
            title: '编辑问题',
            auth: ['questions', 'topic', 'change']
        },
        '/detail/topics/:id/': {
            component: TopicDetail,
            name: 'topic-detail',
            title: '问题详情',
            auth: ['questions', 'topic', 'view']
        },
        '/financeSummary/': {
            component: StockFutures,
            name: 'finance-summary',
            title: '交易信息汇总'
        },
        '/finance': {
            component: Finance,
            subRoutes: {
                '/:product/': {
                    component: FinanceList,
                    title: function () {
                        return consts.finance_product_verbose[this.params.product]
                    },
                    validator: {
                        product: /^(stocks|bonds|futures)$/
                    }
                },
                '/': {
                    component: FinanceIndex,
                    name: 'finance-index',
                    title: '金融'
                }
            }
        },
        '/ram/': {
            component: RAM,
            name: 'ram-index',
            title: '能源与原材料'
        },
        '*': {
            component: NotFound,
            title: '走错路了～'
        }
    })

    router.redirect({
        '/articles/': `/articles/${consts.ArticleType.government}/`
    })

    // validation
    router.beforeEach(({ to, next, abort }) => {
        _.forEach(to.validator || {}, (regexp, key) => {
            if (!regexp.test(to.params[key])) abort()
        })
        next()
    })

    router.beforeEach(function ({ to, next, redirect, abort }) {
        if (to.name === 'login') {
            next()
            return
        }
        checkHasLogined(store)
            .then(logined => {
                if (logined) return logined

                redirect('/login/')
            })
            .then(() => {
                if (to.auth) {
                    let args = to.auth

                    if (to.id) args = args.slice(0, -1).concat([to.id]).concat(args.slice(-1))
                    return getPerm(store, ...args)
                        .then(yes => yes ? next() : abort())
                } else next()
            })
    })

    router.beforeEach(function ({ to, next }) {
        let title = to.title

        switch (true) {
            case _.isFunction(title):
                title = title.call(to)
                break;
            default:
                title = title || '无标题';
        }
        document.title = `${title} - WiseCity`
        next()
    })

    router.beforeEach(() => {
        window.scrollTo(0, 0)
    })

    return router
}