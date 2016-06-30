<template>
    <div class="rows" v-for="article in articles">
        <article-item :article="article"></article-item>
        <infinite-loading :on-infinite="onInfinite"></infinite-loading>
    </div>
</template>

<script>
    import ArticleItem from '../items/ArticleItem.vue'
    import InfiniteLoading from 'vue-infinite-loading'

    export default {
        components: {ArticleItem, InfiniteLoading},
        data: () => ({
            articles: []
        }),
        ready () {
            this.$http.get('/api/articles/')
                .then((res) => {
                    this.articles = res.data.results
                })
        }
    }
</script>