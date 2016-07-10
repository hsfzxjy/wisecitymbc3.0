<template>
    <div class="container article-main">
        <article class="article col-md-8">
            <h1 class="article-title">
                {{ article.title }}
            </h1>
            <div class="article-content">
                {{{ article.content }}}
            </div>
        </article>       
        <article-nav-bar class="col-md-4" vertical :current-category="article.article_type"></article-nav-bar>
    </div>
</template>

<script> 
    import DetailMixin from 'mixins/DetailMixin.es'
    import ArticleNavBar from './ArticleNavBar.vue'
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