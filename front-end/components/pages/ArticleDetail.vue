<template>
    <div class="container">
        <article-nav-bar></article-nav-bar>
        <vs-card>
            <div class="card-block">
                <h1 class="card-title text-center">{{ article.title }}</h1>
                <p class="card-text">
                    {{{ article.content }}}
                </p>
            </div>
        </vs-card>        
    </div>
</template>

<script>
    import { StrUtils } from 'utils/index.es'
    import ArticleNavBar from 'components/navs/ArticleNavBar.vue'
    export default {
        components: {ArticleNavBar},
        data: () => ({
            id: null,
            article: {}
        }),
        route: {
            canActivate (transition) {
                return StrUtils.isDigits(transition.to.params.id)
            },
            data (transition) {
                let id = transition.to.params.id
                return this.$http.get(`/api/articles/${id}/`)
                    .then((res) => ({ article: res.data, id }))
            }
        }
    }
</script>