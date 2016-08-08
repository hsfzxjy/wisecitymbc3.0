<template>
    <div class="article-list sm-no-padding">
        <article-item 
            v-for="article in articles" 
            :article="article"
            :list.sync="articles"
            :index="$index"
            track-by="$index">    
        </article-item>
    </div>
    <list
        :model.sync="articles"
        url="/api/articles/"
        :params="params"
        :autoload="autoload">
    </list>
</template>

<style>
    .article-list {
        padding: 0.9375rem;
    }
</style>

<script>
    import { articles } from 'consts.es'
    import ArticleItem from './ArticleItem.vue'

    export default {
        components: { ArticleItem },
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
            autoload: {
                type: Boolean,
                default: false
            }
        }
    }
</script>