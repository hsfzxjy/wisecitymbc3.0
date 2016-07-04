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
    import DetailMixin from 'components/mixins/DetailMixin.es'
    import ArticleNavBar from 'components/navs/ArticleNavBar.vue'
    export default {
        components: {ArticleNavBar},
        mixins: [DetailMixin],
        data: () => ({
            id: null,
            article: {}
        }),
        detailConfig: {
            baseURL: `/api/articles/`,
            objectFieldName: 'article',
            idFieldName: 'id'
        }
    }
</script>