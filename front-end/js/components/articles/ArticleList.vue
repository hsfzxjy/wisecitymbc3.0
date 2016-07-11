<template>
    <div class="article-list sm-no-padding">
        <article-item 
            v-for="article in articles" 
            :article="article" 
            track-by="$index">    
        </article-item>
    </div>
    <infinite-loading :on-infinite="load"></infinite-loading>
</template>

<style>
    .article-list {
        padding: 0.9375rem;
    }
</style>

<script>
    import { articles } from 'consts.es'
    import ArticleItem from './ArticleItem.vue'
    import InfiniteLoadingMixin from 'mixins/InfiniteLoadingMixin.es'

    export default {
        listConfig: {
            listFieldName: 'articles'
        },
        components: {ArticleItem},
        mixins: [InfiniteLoadingMixin],
        data: () => ({
            articles: [],
            nextURL: ''
        }),
        computed: {
            baseURL () {
                return `/api/articles/`
            },
            params () {
                let params = {}

                if (this.category) 
                    params.article_type = articles.ArticleType[this.category]

                return _.assign(params, this.otherParams)
            }
        },
        props: {
            category: {
                type: String
            },
            otherParams: {
                type: Object
            },
            once: {
                type: Boolean,
                default: false
            }
        },
        watch: {
            category () {
                this.reset()
            }
        },
        events: {
            ['ArticleList:reset'] () {
                this.reset()
            }
        }
    }
</script>