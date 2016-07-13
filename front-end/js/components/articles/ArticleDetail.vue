<template>
    <div class="container article-main">
        <article class="article col-md-8" v-if="!$loadingRouteData">
            <h1 class="article-title">
                {{ article.title }}
            </h1>
            <p class="article-meta">
                {{{ article.author | user }}}
                写于 
                {{ article.created_time | timesince }}
                <a
                    v-link="'/edit/articles/'+id+'/'"
                    v-if="article.perms.change">
                    编辑
                </a>
            </p>
            <hr>
            <div class="article-content">
                {{{ article.content }}}
            </div>
        </article>       
        <article-nav-bar class="col-md-4 hidden-sm-down" vertical :current-category="article.article_type"></article-nav-bar>
    </div>
</template>

<style scoped>
    
</style>

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